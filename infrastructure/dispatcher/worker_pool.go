package main

import (
	"context"
	"fmt"
	"sync"
	"time"

	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/rest"
)

// Job represents a production task
type Job struct {
	ID     string
	Intent string
	MuseID string
}

// WorkerPool manages high-concurrency job distribution
type WorkerPool struct {
	MaxWorkers int
	JobQueue   chan Job
	wg         sync.WaitGroup
	quit       chan bool
	clientset  *kubernetes.Clientset
}

func NewWorkerPool(maxWorkers int) *WorkerPool {
	// Initialize K8s client
	config, err := rest.InClusterConfig()
	if err != nil {
		fmt.Printf("DISPATCHER: Running outside cluster or missing RBAC. Falling back to simulation mode: %v\n", err)
	}

	var clientset *kubernetes.Clientset
	if config != nil {
		clientset, _ = kubernetes.NewForConfig(config)
	}

	return &WorkerPool{
		MaxWorkers: maxWorkers,
		JobQueue:   make(chan Job, 1000),
		quit:       make(chan bool),
		clientset:  clientset,
	}
}

func (wp *WorkerPool) Start() {
	fmt.Printf("DISPATCHER: Starting worker pool with %d slots...\n", wp.MaxWorkers)
	for i := 0; i < wp.MaxWorkers; i++ {
		wp.wg.Add(1)
		go wp.worker(i)
	}
}

func (wp *WorkerPool) worker(id int) {
	defer wp.wg.Done()
	for {
		select {
		case job := <-wp.JobQueue:
			fmt.Printf("Worker %d: Processing intent '%s' for Muse %s [Job: %s]\n", id, job.Intent, job.MuseID, job.ID)
			
			// LOGIC: Scaling Trigger
			if len(wp.JobQueue) > wp.MaxWorkers*2 {
				go wp.CloneMultiplePods(2)
			}

			// In a real implementation, this would call the REST API of the restored Python pod
			time.Sleep(500 * time.Millisecond)
			fmt.Printf("Worker %d: Task %s completed.\n", id, job.ID)

		case <-wp.quit:
			return
		}
	}
}

func (wp *WorkerPool) CloneMultiplePods(count int) {
	if wp.clientset == nil {
		fmt.Printf("GKE_SIMULATION: Burst pressure detected. Cloning %d pods (Mock)...\n", count)
		time.Sleep(2400 * time.Millisecond)
		return
	}

	fmt.Printf("GKE_API: Scaling up %d clones from Golden Agent via Checkpointing...\n", count)
	
	// REAL GKE LOGIC:
	// 1. Trigger Checkpoint on the Golden Pod
	// 2. This is typically done via an annotation update or a custom CRD 
	// for the GKE Checkpoint Restore feature (available in GKE 1.30+).
	
	ctx := context.TODO()
	namespace := "default"
	
	// Example: Updating replicas on the Snapshot-ready deployment
	deploy, err := wp.clientset.AppsV1().Deployments(namespace).Get(ctx, "smos-agents-deployment", metav1.GetOptions{})
	if err == nil {
		newReplicas := *deploy.Spec.Replicas + int32(count)
		deploy.Spec.Replicas = &newReplicas
		_, err = wp.clientset.AppsV1().Deployments(namespace).Update(ctx, deploy, metav1.UpdateOptions{})
		if err != nil {
			fmt.Printf("GKE_API ERROR: Failed to scale: %v\n", err)
		} else {
			fmt.Printf("GKE_API: Scaling smos-agents-deployment to %d replicas.\n", newReplicas)
		}
	}
}

func (wp *WorkerPool) Stop() {
	close(wp.quit)
	wp.wg.Wait()
}
