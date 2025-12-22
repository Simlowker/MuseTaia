package main

import (
	"testing"
	"time"
)

func test_worker_pool(t *testing.T) {
	pool := NewWorkerPool(2)
	pool.Start()

	job := Job{ID: "test-1", Intent: "Test production"}
	pool.JobQueue <- job

	// Allow some time for processing
	time.Sleep(100 * time.Millisecond)
	
	pool.Stop()
}
