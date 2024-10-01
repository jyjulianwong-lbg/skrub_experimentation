FROM python:3.12.3

# It’s often recommended to set this environment variable when running Python within Docker containers to ensure that Python doesn’t buffer the output.
ENV PYTHONUNBUFFERED 1
ARG PY_INDEX=https://nexus.mgmt-bld.oncp.dev/repository/python-proxy/pypi
ARG PY_INDEX_URL=https://nexus.mgmt-bld.oncp.dev/repository/python-proxy/simple

WORKDIR /usr/src/app

# Mount SSL certificates for Internet access.
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
COPY wss.crt /root/wss.crt
RUN cat /root/wss.crt >> /etc/ssl/certs/ca-certificates.crt && cp /root/wss.crt /usr/local/share/ca-certificates/wss.crt

# Install dependences first to make caching more efficient.
COPY requirements.txt ./
RUN pip install --no-compile --no-cache-dir --no-deps -r requirements.txt --index=$PY_INDEX --index-url=$PY_INDEX_URL

# Copy the rest of the source code.
COPY . .

# Run the module.
CMD [ "python", "-m", "reconciler" ]