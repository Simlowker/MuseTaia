# SMOS v2 Dispatcher Dockerfile
FROM golang:1.21-alpine AS builder

WORKDIR /app

# Install system dependencies
RUN apk add --no-cache git

# 1. Copy source code (including go.mod)
COPY . .

# 2. Tidy dependencies (generates go.sum and updates go.mod based on source usage)
RUN go mod tidy

# 3. Build the application
RUN CGO_ENABLED=0 GOOS=linux go build -o smos-dispatcher .

# Final stage
FROM alpine:latest
WORKDIR /root/
COPY --from=builder /app/smos-dispatcher .

# Set entry point
CMD ["./smos-dispatcher"]
