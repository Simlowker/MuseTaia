package main

import (
	"fmt"
	"log"
	"net/http"
)

func main() {
	fmt.Println("--- SMOS Magic Factory Dispatcher (Infrastructure v2) ---")
	
	// Initialize Worker Pool (Capacity based on GKE node limits)
	pool := NewWorkerPool(20)
	pool.Start()

	server := NewDispatcherServer(pool)

	// Route Handlers
	http.HandleFunc("/health", server.HandleHealth)
	http.HandleFunc("/dispatch", server.HandleDispatch)

	port := "8080"
	fmt.Printf("DISPATCHER: High-concurrency listener active on :%s\n", port)
	log.Fatal(http.ListenAndServe(":