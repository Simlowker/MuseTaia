# SMOS v2 Dispatcher Dockerfile
FROM golang:1.21-alpine AS builder

WORKDIR /app

# Install system dependencies
RUN apk add --no-cache git

# 1. Copy dependency files first (Optimizes Docker layer cache)
COPY go.mod ./

# 2. Download dependencies
RUN go mod download

# 3. Copy source code and build
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o smos-dispatcher .

# Final stage
FROM alpine:latest
WORKDIR /root/
COPY --from=builder /app/smos-dispatcher .

# Set entry point
CMD ["./smos-dispatcher"]
