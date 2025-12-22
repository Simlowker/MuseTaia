package main

import (
	"fmt"
	"log"
	"net/http"
)

func main() {
	fmt.Println("Initializing SMOS Magic Factory Dispatcher...")
	
	// Initialize Worker Pool (e.g., 10 concurrent workers)
	pool := NewWorkerPool(10)
	pool.Start()

	server := NewDispatcherServer(pool)

	// Basic health check
	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "Dispatcher is healthy")
	})

	// Dispatch endpoint
	http.HandleFunc("/dispatch", server.HandleDispatch)

	fmt.Println("Dispatcher listening on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
