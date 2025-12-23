# SMOS v2 Dispatcher Dockerfile
FROM golang:1.21-alpine AS builder

WORKDIR /app

# Install system dependencies
RUN apk add --no-cache git

# Copy go mod and sum
COPY go.mod ./
# Note: go.sum will be generated if missing
RUN go mod tidy

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
