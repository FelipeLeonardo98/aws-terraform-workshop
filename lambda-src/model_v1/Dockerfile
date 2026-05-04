FROM public.ecr.aws/lambda/python:3.14

# Set working directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Install dependencies directly with pip
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    pandas>=3.0.0 \
    scikit-learn>=1.8.0 \
    matplotlib>=3.10.8 \
    seaborn>=0.13.2 \
    plotly>=6.5.2 \
    nbformat>=5.10.4 \
    numpy>=2.4.4 \
    joblib

# Copy the application and model file
COPY app.py .
COPY lr_model_iris_v1.joblib .

# Verify model file exists
RUN ls -la ${LAMBDA_TASK_ROOT}

# Set the Lambda handler
CMD ["app.handler"]