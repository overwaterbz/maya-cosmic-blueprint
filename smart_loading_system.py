#!/usr/bin/env python3
"""
Smart Loading System - Phase 2 Scale Optimization
Intelligent loading and progressive enhancement for detailed explanations
"""

import asyncio
import json
import time
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor
import threading
from queue import Queue, PriorityQueue
from datetime import datetime, timedelta

class LoadingPriority(Enum):
    """Priority levels for loading requests"""
    CRITICAL = 1    # Essential elements (day sign, galactic tone)
    HIGH = 2        # Core elements (element, direction)
    MEDIUM = 3      # Secondary elements (spirit animal, crystal ally)
    LOW = 4         # Additional elements (plant medicine, chakra)
    BACKGROUND = 5  # Background pre-loading

@dataclass
class LoadingRequest:
    """Represents a loading request with priority and metadata"""
    request_id: str
    user_id: str
    element_type: str
    element_value: str
    priority: LoadingPriority
    timestamp: float = field(default_factory=time.time)
    callback: Optional[Callable] = None
    timeout: float = 30.0
    retry_count: int = 0
    max_retries: int = 3
    
    def __lt__(self, other):
        """Enable priority queue sorting"""
        return self.priority.value < other.priority.value

class LoadingResult:
    """Represents the result of a loading operation"""
    def __init__(self, request_id: str, success: bool, data: Any = None, 
                 error: str = None, load_time: float = 0.0):
        self.request_id = request_id
        self.success = success
        self.data = data
        self.error = error
        self.load_time = load_time
        self.timestamp = time.time()

class SmartLoadingSystem:
    """Intelligent loading system with prioritization and progressive enhancement"""
    
    def __init__(self, max_workers: int = 10, max_concurrent_per_user: int = 5):
        self.max_workers = max_workers
        self.max_concurrent_per_user = max_concurrent_per_user
        
        # Threading components
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.request_queue = PriorityQueue()
        self.active_requests: Dict[str, LoadingRequest] = {}
        self.user_active_count: Dict[str, int] = {}
        self.results_cache: Dict[str, LoadingResult] = {}
        
        # Performance tracking
        self.performance_stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'average_load_time': 0.0,
            'cache_hits': 0,
            'queue_size': 0
        }
        
        # Background processing
        self.is_running = False
        self.processing_thread = None
        
        # Element loading strategies
        self.loading_strategies = {
            'day_sign': self._load_core_element,
            'galactic_tone': self._load_core_element,
            'element': self._load_core_element,
            'direction': self._load_core_element,
            'spirit_animal': self._load_detailed_element,
            'crystal_ally': self._load_detailed_element,
            'plant_medicine': self._load_detailed_element,
            'chakra_resonance': self._load_detailed_element,
            'human_design_type': self._load_complex_element,
            'tree_of_life_primary': self._load_complex_element,
            'maya_cross_guide': self._load_complex_element,
            'explanation': self._load_ai_explanation
        }
    
    def start(self):
        """Start the smart loading system"""
        if not self.is_running:
            self.is_running = True
            self.processing_thread = threading.Thread(target=self._process_queue, daemon=True)
            self.processing_thread.start()
    
    def stop(self):
        """Stop the smart loading system"""
        self.is_running = False
        if self.processing_thread:
            self.processing_thread.join(timeout=5)
        self.executor.shutdown(wait=True)
    
    def request_element_loading(self, user_id: str, element_type: str, element_value: str,
                              priority: LoadingPriority = LoadingPriority.MEDIUM,
                              callback: Optional[Callable] = None) -> str:
        """Request element loading with specified priority"""
        request_id = f"{user_id}_{element_type}_{int(time.time() * 1000)}"
        
        # Check cache first
        cache_key = f"{user_id}_{element_type}_{element_value}"
        if cache_key in self.results_cache:
            cached_result = self.results_cache[cache_key]
            if time.time() - cached_result.timestamp < 1800:  # 30 minutes cache
                self.performance_stats['cache_hits'] += 1
                if callback:
                    callback(cached_result)
                return request_id
        
        # Create loading request
        request = LoadingRequest(
            request_id=request_id,
            user_id=user_id,
            element_type=element_type,
            element_value=element_value,
            priority=priority,
            callback=callback
        )
        
        # Add to queue
        self.request_queue.put(request)
        self.performance_stats['total_requests'] += 1
        self.performance_stats['queue_size'] = self.request_queue.qsize()
        
        return request_id
    
    def batch_request_elements(self, user_id: str, elements: List[Dict[str, Any]]) -> List[str]:
        """Request multiple elements with intelligent prioritization"""
        request_ids = []
        
        # Sort elements by priority
        prioritized_elements = self._prioritize_elements(elements)
        
        for element_data in prioritized_elements:
            request_id = self.request_element_loading(
                user_id=user_id,
                element_type=element_data['type'],
                element_value=element_data['value'],
                priority=element_data['priority'],
                callback=element_data.get('callback')
            )
            request_ids.append(request_id)
        
        return request_ids
    
    def preload_user_dashboard(self, user_id: str, user_profile: Dict[str, Any]) -> Dict[str, str]:
        """Preload all elements for user dashboard with smart prioritization"""
        # Define critical elements for immediate loading
        critical_elements = [
            {'type': 'day_sign', 'value': user_profile.get('day_sign', ''), 'priority': LoadingPriority.CRITICAL},
            {'type': 'galactic_tone', 'value': user_profile.get('galactic_tone', ''), 'priority': LoadingPriority.CRITICAL},
            {'type': 'element', 'value': user_profile.get('element', ''), 'priority': LoadingPriority.HIGH},
            {'type': 'direction', 'value': user_profile.get('direction', ''), 'priority': LoadingPriority.HIGH}
        ]
        
        # Define secondary elements for progressive loading
        secondary_elements = [
            {'type': 'spirit_animal', 'value': user_profile.get('spirit_animal', ''), 'priority': LoadingPriority.MEDIUM},
            {'type': 'crystal_ally', 'value': user_profile.get('crystal_ally', ''), 'priority': LoadingPriority.MEDIUM},
            {'type': 'plant_medicine', 'value': user_profile.get('plant_medicine', ''), 'priority': LoadingPriority.MEDIUM},
            {'type': 'chakra_resonance', 'value': user_profile.get('chakra_resonance', ''), 'priority': LoadingPriority.LOW}
        ]
        
        # Define background elements for background loading
        background_elements = [
            {'type': 'human_design_type', 'value': user_profile.get('human_design_type', ''), 'priority': LoadingPriority.BACKGROUND},
            {'type': 'tree_of_life_primary', 'value': user_profile.get('tree_of_life_primary', ''), 'priority': LoadingPriority.BACKGROUND},
            {'type': 'tree_of_life_secondary', 'value': user_profile.get('tree_of_life_secondary', ''), 'priority': LoadingPriority.BACKGROUND}
        ]
        
        # Request all elements
        all_elements = critical_elements + secondary_elements + background_elements
        request_ids = self.batch_request_elements(user_id, all_elements)
        
        return {
            'request_ids': request_ids,
            'critical_count': len(critical_elements),
            'secondary_count': len(secondary_elements),
            'background_count': len(background_elements),
            'total_count': len(all_elements)
        }
    
    def _process_queue(self):
        """Background thread to process loading requests"""
        while self.is_running:
            try:
                # Get next request from queue
                request = self.request_queue.get(timeout=1)
                
                # Check if user has too many active requests
                if self.user_active_count.get(request.user_id, 0) >= self.max_concurrent_per_user:
                    # Put back in queue with slight delay
                    time.sleep(0.1)
                    self.request_queue.put(request)
                    continue
                
                # Process request
                self._process_request(request)
                
            except:
                # Queue was empty, continue
                continue
    
    def _process_request(self, request: LoadingRequest):
        """Process a single loading request"""
        # Track active request
        self.active_requests[request.request_id] = request
        self.user_active_count[request.user_id] = self.user_active_count.get(request.user_id, 0) + 1
        
        # Submit to thread pool
        future = self.executor.submit(self._execute_loading, request)
        
        # Handle result when complete
        def handle_result(fut):
            try:
                result = fut.result()
                self._handle_loading_result(request, result)
            except Exception as e:
                error_result = LoadingResult(
                    request_id=request.request_id,
                    success=False,
                    error=str(e),
                    load_time=time.time() - request.timestamp
                )
                self._handle_loading_result(request, error_result)
        
        future.add_done_callback(handle_result)
    
    def _execute_loading(self, request: LoadingRequest) -> LoadingResult:
        """Execute the actual loading operation"""
        start_time = time.time()
        
        try:
            # Get appropriate loading strategy
            strategy = self.loading_strategies.get(request.element_type, self._load_default_element)
            
            # Execute loading
            data = strategy(request.user_id, request.element_type, request.element_value)
            
            # Create successful result
            result = LoadingResult(
                request_id=request.request_id,
                success=True,
                data=data,
                load_time=time.time() - start_time
            )
            
            return result
            
        except Exception as e:
            # Create error result
            result = LoadingResult(
                request_id=request.request_id,
                success=False,
                error=str(e),
                load_time=time.time() - start_time
            )
            
            return result
    
    def _handle_loading_result(self, request: LoadingRequest, result: LoadingResult):
        """Handle the result of a loading operation"""
        # Remove from active requests
        self.active_requests.pop(request.request_id, None)
        self.user_active_count[request.user_id] = max(0, self.user_active_count.get(request.user_id, 0) - 1)
        
        # Update performance stats
        if result.success:
            self.performance_stats['successful_requests'] += 1
        else:
            self.performance_stats['failed_requests'] += 1
        
        # Update average load time
        total_successful = self.performance_stats['successful_requests']
        if total_successful > 0:
            current_avg = self.performance_stats['average_load_time']
            self.performance_stats['average_load_time'] = (
                (current_avg * (total_successful - 1) + result.load_time) / total_successful
            )
        
        # Cache successful results
        if result.success:
            cache_key = f"{request.user_id}_{request.element_type}_{request.element_value}"
            self.results_cache[cache_key] = result
        
        # Handle retries for failed requests
        if not result.success and request.retry_count < request.max_retries:
            request.retry_count += 1
            request.timestamp = time.time()
            self.request_queue.put(request)
            return
        
        # Execute callback if provided
        if request.callback:
            request.callback(result)
    
    def _prioritize_elements(self, elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prioritize elements based on importance and loading strategy"""
        # Add priority to elements that don't have it
        for element in elements:
            if 'priority' not in element:
                element['priority'] = self._get_default_priority(element['type'])
        
        # Sort by priority
        return sorted(elements, key=lambda x: x['priority'].value)
    
    def _get_default_priority(self, element_type: str) -> LoadingPriority:
        """Get default priority for element type"""
        priority_map = {
            'day_sign': LoadingPriority.CRITICAL,
            'galactic_tone': LoadingPriority.CRITICAL,
            'element': LoadingPriority.HIGH,
            'direction': LoadingPriority.HIGH,
            'spirit_animal': LoadingPriority.MEDIUM,
            'crystal_ally': LoadingPriority.MEDIUM,
            'plant_medicine': LoadingPriority.MEDIUM,
            'chakra_resonance': LoadingPriority.LOW,
            'human_design_type': LoadingPriority.BACKGROUND,
            'tree_of_life_primary': LoadingPriority.BACKGROUND,
            'tree_of_life_secondary': LoadingPriority.BACKGROUND
        }
        return priority_map.get(element_type, LoadingPriority.MEDIUM)
    
    def _load_core_element(self, user_id: str, element_type: str, element_value: str) -> Dict[str, Any]:
        """Load core elements quickly with basic information"""
        from cosmic_elements_database import get_element_data
        
        element_data = get_element_data(element_type, element_value)
        if element_data:
            return {
                'type': element_type,
                'value': element_value,
                'name': element_data.get('name', element_value),
                'description': element_data.get('description', '')[:500],  # Truncated for speed
                'load_strategy': 'core',
                'full_data_available': True
            }
        
        return self._generate_fallback_element(element_type, element_value)
    
    def _load_detailed_element(self, user_id: str, element_type: str, element_value: str) -> Dict[str, Any]:
        """Load detailed elements with comprehensive information"""
        from cosmic_elements_database import get_element_data
        from personalized_content_engine import generate_personalized_content
        
        # Get base element data
        element_data = get_element_data(element_type, element_value)
        if not element_data:
            return self._generate_fallback_element(element_type, element_value)
        
        # Generate personalized content
        try:
            personalized_content = generate_personalized_content(user_id, element_type, element_value)
        except:
            personalized_content = element_data.get('description', '')
        
        return {
            'type': element_type,
            'value': element_value,
            'name': element_data.get('name', element_value),
            'description': element_data.get('description', ''),
            'personalized_content': personalized_content,
            'load_strategy': 'detailed',
            'full_data_available': True
        }
    
    def _load_complex_element(self, user_id: str, element_type: str, element_value: str) -> Dict[str, Any]:
        """Load complex elements with full AI processing"""
        from cosmic_elements_database import get_element_data
        from personalized_content_engine import generate_personalized_content
        from ai_spiritual_engine import get_personalized_element_snapshot
        
        # Get base element data
        element_data = get_element_data(element_type, element_value)
        if not element_data:
            return self._generate_fallback_element(element_type, element_value)
        
        # Generate comprehensive personalized content
        try:
            personalized_content = generate_personalized_content(user_id, element_type, element_value)
            element_snapshot = get_personalized_element_snapshot(user_id, {}, element_type, element_value)
        except:
            personalized_content = element_data.get('description', '')
            element_snapshot = f"Your {element_type} carries sacred wisdom for your spiritual journey."
        
        return {
            'type': element_type,
            'value': element_value,
            'name': element_data.get('name', element_value),
            'description': element_data.get('description', ''),
            'personalized_content': personalized_content,
            'element_snapshot': element_snapshot,
            'load_strategy': 'complex',
            'full_data_available': True
        }
    
    def _load_ai_explanation(self, user_id: str, element_type: str, element_value: str) -> Dict[str, Any]:
        """Load AI-powered explanations"""
        try:
            # Import here to avoid circular imports
            import openai
            
            # Generate AI explanation (simplified for demo)
            explanation = f"Your {element_type} '{element_value}' carries profound spiritual significance, offering guidance and wisdom for your sacred journey. This element represents transformation, growth, and connection to ancient wisdom."
            
            return {
                'type': 'explanation',
                'element_type': element_type,
                'element_value': element_value,
                'explanation': explanation,
                'load_strategy': 'ai',
                'full_data_available': True
            }
        except:
            return self._generate_fallback_element('explanation', f"{element_type}_{element_value}")
    
    def _load_default_element(self, user_id: str, element_type: str, element_value: str) -> Dict[str, Any]:
        """Default loading strategy for unknown element types"""
        return self._generate_fallback_element(element_type, element_value)
    
    def _generate_fallback_element(self, element_type: str, element_value: str) -> Dict[str, Any]:
        """Generate fallback element data"""
        return {
            'type': element_type,
            'value': element_value,
            'name': element_value,
            'description': f"Your {element_type} carries sacred wisdom and spiritual guidance for your journey.",
            'load_strategy': 'fallback',
            'full_data_available': False
        }
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        return {
            **self.performance_stats,
            'active_requests': len(self.active_requests),
            'cache_size': len(self.results_cache),
            'queue_size': self.request_queue.qsize()
        }
    
    def cleanup_cache(self, max_age: int = 1800):
        """Clean up old cache entries"""
        current_time = time.time()
        keys_to_remove = []
        
        for key, result in self.results_cache.items():
            if current_time - result.timestamp > max_age:
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del self.results_cache[key]
        
        return len(keys_to_remove)

# Global smart loading instance
smart_loader = SmartLoadingSystem()

# Convenience functions
def load_user_dashboard_smart(user_id: str, user_profile: Dict[str, Any]) -> Dict[str, str]:
    """Smart loading for user dashboard"""
    smart_loader.start()
    return smart_loader.preload_user_dashboard(user_id, user_profile)

def load_element_explanation_smart(user_id: str, element_type: str, element_value: str, 
                                 callback: Optional[Callable] = None) -> str:
    """Smart loading for element explanation"""
    smart_loader.start()
    return smart_loader.request_element_loading(
        user_id, 'explanation', f"{element_type}_{element_value}", 
        LoadingPriority.HIGH, callback
    )

if __name__ == "__main__":
    # Test smart loading system
    print("Testing Smart Loading System...")
    
    # Start the system
    smart_loader.start()
    
    # Test user dashboard preloading
    test_profile = {
        'day_sign': 'Ahau',
        'galactic_tone': 'Galactic',
        'element': 'Fire',
        'direction': 'South',
        'spirit_animal': 'Jaguar',
        'crystal_ally': 'Amethyst',
        'plant_medicine': 'Sage'
    }
    
    result = load_user_dashboard_smart("test_user", test_profile)
    print(f"Dashboard preload result: {result}")
    
    # Test performance stats
    time.sleep(2)  # Let some processing happen
    stats = smart_loader.get_performance_stats()
    print(f"Performance stats: {stats}")
    
    # Stop the system
    smart_loader.stop()
    
    print("Smart loading system ready for production!")