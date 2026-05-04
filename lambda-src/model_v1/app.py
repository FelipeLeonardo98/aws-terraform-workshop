import numpy as np
from typing  import Any
import joblib
import logging
import json

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load model once at container startup (outside handler for warm starts)
model = None
model_metrics = {}

try:
    logger.info("Loading model at startup...")
    model = joblib.load('lr_model_iris_v1.joblib')
    logger.info("Model loaded successfully")
    
    # Extract model metrics if available
    model_metrics = {
        "model_type": type(model).__name__,
        "n_features": model.n_features_in_ if hasattr(model, 'n_features_in_') else None,
        "classes": model.classes_.tolist() if hasattr(model, 'classes_') else None,
    }
    logger.info(f"Model metrics: {model_metrics}")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    model = None

def predict_single(model: Any, request: dict) -> dict:
    # enforce 2D matrix
    X = np.array(request["sample"]).reshape(1, -1)
    pred = model.predict(X)[0]
    proba = model.predict_proba(X)[0]

    return {
        "class": int(pred),
        "probabilities": proba.tolist()
    }

def predict_pretty(model: Any, request: dict) -> dict:

    dict_species = {
        0: "setosa",
        1: "versicolor",
        2: "virginica"
    }
    
    # 🔹 Ideal: manter ordem fixa das features (produção)
    feature_order = [
        "sepal length (cm)",
        "sepal width (cm)",
        "petal length (cm)",
        "petal width (cm)"
    ]

    # 🔹 Mapear entrada garantindo ordem correta
    feature_list = [request["user_readable"][f] for f in feature_order]

    X = np.array(feature_list).reshape(1, -1)

    pred = model.predict(X)[0]

    # adjust number format
    proba = model.predict_proba(X)[0].astype(float).tolist()
    proba = [float( round(p,2) ) for p in proba]

    # 🔹 Usa classes do próprio modelo (melhor prática)
    classes = model.classes_

    mapped = {
        dict_species[int(k)]: v
        for k, v in zip(classes, proba)
    }

    # 🔹 Ordenar probabilidades (UX melhor)
    sorted_probs = dict(
        sorted(mapped.items(), key=lambda x: x[1], reverse=True)
    )

    # Get prediction confidence (highest probability)
    confidence = max(proba)

    return {
        "class": dict_species[int(pred)],
        "probabilities": sorted_probs,
        "confidence": round(confidence, 2),
        "model_metrics": {
            "model_type": model_metrics.get("model_type"),
            "n_features": model_metrics.get("n_features"),
            "prediction_confidence": round(confidence, 2)
        }
    }

def handler(event, context):
    """
    Lambda handler function
    event: Contains the input data from the API call
    context: Lambda context object with request metadata
    """
    try:
        if model is None:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Model failed to load'})
            }
        
        # Extract Lambda context information
        lambda_version = context.function_version if hasattr(context, 'function_version') else 'unknown'
        request_id = context.aws_request_id if hasattr(context, 'aws_request_id') else 'unknown'
        
        logger.info(f"Lambda Function Version: {lambda_version}, Request ID: {request_id}")
        
        # Parse event - supports both direct parameters and API Gateway format
        if 'body' in event:
            # API Gateway format
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        else:
            # Direct invocation
            body = event
        
        # Check if user provided features in different formats
        if 'user_readable' in body:
            predict_result = predict_pretty(model=model, request=body)
            # Add Lambda version to pretty response
            predict_result['lambda_version'] = lambda_version
            predict_result['request_id'] = request_id
        else:
            predict_result = predict_single(model=model, request=body)
            # Add Lambda version to single response
            predict_result['lambda_version'] = lambda_version
            predict_result['request_id'] = request_id
        
        return {
            'statusCode': 200,
            'body': json.dumps(predict_result)
        }
    except Exception as e:
        logger.error(f"Error during prediction: {e}", exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

if __name__ == '__main__':
    # Local testing
    logger.info("Testing handler locally...")
    
    test_event = {
        "sample": [6.9, 3.1, 4.9, 1.5]
    }
    
    test_context = type('obj', (object,), {
        'function_name': 'test',
        'aws_request_id': 'test-request-id'
    })()
    
    result = handler(test_event, test_context)
    logger.info(f"Result: {result}")
