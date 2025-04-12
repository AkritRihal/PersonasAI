FROM python:3.11-slim

# Create a non-root user
RUN useradd -m -u 1000 user
USER user

# Set the working directory
WORKDIR /home/user

# Set environment variables
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Copy project files and install dependencies
COPY --chown=user:user . /home/user
COPY requirements.txt /home/user
RUN pip install --no-cache-dir --user -r requirements.txt

# Run the application
CMD ["chainlit", "run", "persona.py", "--port", "7860"]