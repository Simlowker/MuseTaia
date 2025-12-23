package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"time"
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
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	if job.ID == "" {
		job.ID = fmt.Sprintf("job-%d", time.Now().UnixNano())
	}

	// Logic: If VVS > 90, trigger 'Massive Parallelism' (Burst)
	// (VVS would typically be passed in parameters or intent)
	if time.Now().UnixNano()%2 == 0 { // Simulation: High priority detection
		fmt.Printf("API: [BURST MODE] High priority detected. Triggering 5x parallel clones.\n")
		go s.pool.CloneMultiplePods(5)
	}

	fmt.Printf("API: Received trigger request for Muse %s (Intent: %s)\n", job.MuseID, job.Intent)


	// Dispatch to worker pool (High Concurrency Channel)
	select {
	case s.pool.JobQueue <- job:
		w.WriteHeader(http.StatusAccepted)
		response := map[string]string{
			"status":  "accepted",
			"job_id":  job.ID,
			"message": fmt.Sprintf("Job queued for Muse %s", job.MuseID),
		}
		json.NewEncoder(w).Encode(response)
default:
		// Channel full, trigger snapshot restore immediately
		go s.pool.CloneMultiplePods(1)
		http.Error(w, "Dispatcher queue full, scaling up...", http.StatusServiceUnavailable)
	}
}

func (s *DispatcherServer) HandleHealth(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "OK - Active Workers: %d", s.pool.MaxWorkers)
}