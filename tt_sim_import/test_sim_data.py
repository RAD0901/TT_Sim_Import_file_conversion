#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for the simulation data handling module.
"""

import os
import unittest
import tempfile
import json
from sim_data import SimulationData

class TestSimulationData(unittest.TestCase):
    """Test cases for the SimulationData class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_data = {
            "simulation_id": "test-001",
            "parameters": {
                "param1": 10.5,
                "param2": "value2"
            },
            "results": [1, 2, 3, 4, 5]
        }
        
        self.test_metadata = {
            "version": "1.0",
            "created": "2025-04-17T10:00:00",
            "format": "json"
        }
        
        self.sim_data = SimulationData(self.test_data, self.test_metadata)
    
    def test_init(self):
        """Test initialization of SimulationData."""
        # Test with data and metadata
        self.assertEqual(self.sim_data.data, self.test_data)
        self.assertEqual(self.sim_data.metadata, self.test_metadata)
        
        # Test default initialization
        default_sim_data = SimulationData()
        self.assertEqual(default_sim_data.data, {})
        self.assertIsNotNone(default_sim_data.metadata)
        self.assertEqual(default_sim_data.metadata["version"], "1.0")
    
    def test_save_and_load_json(self):
        """Test saving and loading JSON data."""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as temp:
            temp_path = temp.name
        
        try:
            # Save data to a temporary file
            self.assertTrue(self.sim_data.save_to_file(temp_path))
            
            # Create a new instance and load the data
            new_sim_data = SimulationData()
            self.assertTrue(new_sim_data.load_from_file(temp_path))
            
            # Verify the data was loaded correctly
            self.assertEqual(new_sim_data.data, self.test_data)
            self.assertEqual(new_sim_data.metadata, self.test_metadata)
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def test_convert_format(self):
        """Test converting data format."""
        # Test format conversion (placeholder test)
        target_format = "csv"
        self.assertTrue(self.sim_data.convert_format(target_format))
        self.assertEqual(self.sim_data.metadata["format"], target_format)

if __name__ == '__main__':
    unittest.main()