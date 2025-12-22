package main

import (
	"encoding/json"
	"fmt"
	"net/http"
)

type DispatcherServer struct {
	pool *WorkerPool
}

func NewDispatcherServer(pool *WorkerPool) *DispatcherServer {
	return &DispatcherServer{pool: pool}
}

func (s *DispatcherServer) HandleDispatch(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var job Job
	if err := json.NewDecoder(r.Body).Decode(&job); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	// Dispatch to worker pool
	s.pool.JobQueue <- job

	w.WriteHeader(http.StatusAccepted)
	fmt.Fprintf(w, "Job %s accepted", job.ID)
}
