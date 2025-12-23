# SMOS v2 Dispatcher Dockerfile
FROM golang:1.21-alpine AS builder

WORKDIR /app

# Install system dependencies
RUN apk add --no-cache git

# Copy go mod and attempt to copy go.sum (ignore error if missing)
COPY go.mod ./
COPY go.sum* ./

# Ensure dependencies are tidy and downloaded
# Note: In Cloud Build, ensure the project has internet access
RUN go mod tidy && go mod download

# Copy source code
COPY . .

# Build the binary
RUN CGO_ENABLED=0 GOOS=linux go build -o smos-dispatcher .

# Final stage
FROM alpine:latest
WORKDIR /root/
COPY --from=builder /app/smos-dispatcher .

# Set entry point
CMD ["./smos-dispatcher"]