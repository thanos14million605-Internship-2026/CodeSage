import joblib
import numpy as np
import pandas as pd
from typing import Dict, List, Any
import os
import logging
from app.utils.feature_extractor import CodeFeatureExtractor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MLService:
    def __init__(self):
        self.model = None
        self.feature_extractor = CodeFeatureExtractor()
        self.feature_names = [
            'loc', 'num_functions', 'cyclomatic_complexity', 
            'nesting_depth', 'num_imports', 'num_classes', 
            'avg_function_length'
        ]
        self.model_loaded = False
        self.load_model()
    
    def load_model(self):
        """Load the trained Random Forest model."""
        try:
            model_path = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    '../../../../model/random_forest_model.pkl'
                )
            )            
            if not os.path.exists(model_path):
                logger.warning(f"Model file not found at {model_path}. Please train and save the model first.")
                self.model_loaded = False
                return False
            
            model_data = joblib.load(model_path)

            # Extract actual model
            self.model = model_data['model']

            # (Optional but recommended)
            self.feature_names = model_data.get('feature_names', self.feature_names)

            self.model_loaded = True
            logger.info("Random Forest model loaded successfully")
            self.model_loaded = True
            logger.info("Random Forest model loaded successfully")
            
            # Log model information
            if hasattr(self.model, 'n_features_'):
                logger.info(f"Model trained on {self.model.n_features_} features")
            if hasattr(self.model, 'feature_importances_'):
                logger.info("Feature importances available")
            
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self.model_loaded = False
            return False
    
    def predict_risk(self, code: str, file_name: str = "unknown.py") -> Dict[str, Any]:
        """Predict bug risk for given code using the trained Random Forest model."""
        
        # Extract features from code
        features = self.feature_extractor.extract_features(code, file_name)
        
        # Check if model is loaded
        if not self.model_loaded or self.model is None:
            raise ValueError("Model not loaded. Please ensure the model file exists and is properly trained.")
        
        try:
            # Prepare feature vector in correct order
            feature_vector = np.array([[features[name] for name in self.feature_names]])
            
            # Make prediction using the trained Random Forest model
            risk_probability = self.model.predict_proba(feature_vector)[0][1]  # Probability of high risk class
            risk_score = float(risk_probability)
            
            # Get prediction class
            prediction_class = self.model.predict(feature_vector)[0]
            
            # Get feature importance if available
            feature_importance = self._get_feature_importance(features)
            
            # Generate recommendations based on model insights
            recommendations = self._generate_model_based_recommendations(features, risk_score, feature_importance)
            
            # Get high-risk functions if available
            high_risk_functions = self._identify_high_risk_functions(code, features)
            
            return {
                'risk_score': risk_score,
                'prediction_class': int(prediction_class),
                'features': features,
                'feature_importance': feature_importance,
                'important_features': self._get_important_features_list(features, feature_importance),
                'recommendations': recommendations,
                'high_risk_functions': high_risk_functions,
                'model_confidence': self._get_prediction_confidence(risk_score)
            }
            
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            raise ValueError(f"Prediction failed: {str(e)}")
    
    def _get_feature_importance(self, features: Dict[str, Any]) -> Dict[str, float]:
        """Get feature importance from the trained model."""
        if self.model is None or not hasattr(self.model, 'feature_importances_'):
            return {}
        
        importance_dict = {}
        for i, feature_name in enumerate(self.feature_names):
            if i < len(self.model.feature_importances_):
                importance_dict[feature_name] = float(self.model.feature_importances_[i])
        
        return importance_dict
    
    def _get_important_features_list(self, features: Dict[str, Any], feature_importance: Dict[str, float]) -> List[str]:
        """Identify most important features contributing to risk based on model insights."""
        important = []
        
        # Use model's feature importance to identify key contributors
        if feature_importance:
            # Sort features by importance
            sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
            
            # Get top 3 most important features
            for feature_name, importance in sorted_features[:3]:
                feature_value = features.get(feature_name, 0)
                
                # Add context based on feature value and importance
                if feature_name == 'cyclomatic_complexity' and feature_value > 10:
                    important.append(f'High cyclomatic complexity ({feature_value:.1f})')
                elif feature_name == 'nesting_depth' and feature_value > 3:
                    important.append(f'Deep nesting depth ({feature_value})')
                elif feature_name == 'avg_function_length' and feature_value > 50:
                    important.append(f'Long average function length ({feature_value:.1f} lines)')
                elif feature_name == 'loc' and feature_value > 200:
                    important.append(f'Large file size ({feature_value} lines)')
                elif feature_name == 'num_functions' and feature_value > 10:
                    important.append(f'High function count ({feature_value})')
                else:
                    important.append(f'{feature_name.replace("_", " ").title()}: {feature_value:.1f}')
        
        return important if important else ['Model analysis completed']
    
    def _generate_model_based_recommendations(self, features: Dict[str, Any], risk_score: float, feature_importance: Dict[str, float]) -> List[str]:
        """Generate recommendations based on model insights and feature importance."""
        recommendations = []
        
        if risk_score > 0.8:
            recommendations.append("High risk detected! Immediate refactoring recommended")
        elif risk_score > 0.6:
            recommendations.append("Moderate risk. Consider code improvements")
        elif risk_score > 0.4:
            recommendations.append("Low to moderate risk. Monitor and optimize")
        else:
            recommendations.append("Low risk detected. Code quality appears good")
        
        # Feature-specific recommendations based on importance
        if feature_importance:
            most_important = max(feature_importance.items(), key=lambda x: x[1])
            
            if most_important[0] == 'cyclomatic_complexity' and features['cyclomatic_complexity'] > 8:
                recommendations.append("Reduce cyclomatic complexity by breaking down complex functions")
            
            if most_important[0] == 'nesting_depth' and features['nesting_depth'] > 2:
                recommendations.append("Reduce nesting depth using early returns and helper functions")
            
            if most_important[0] == 'avg_function_length' and features['avg_function_length'] > 30:
                recommendations.append("Break down long functions into smaller, focused units")
        
        # General recommendations based on feature values
        if features['loc'] > 150:
            recommendations.append("📁 Consider splitting large files into focused modules")
        
        if features['num_imports'] > 15:
            recommendations.append("Review imports for potential dependencies reduction")
        
        if features['num_classes'] > 5:
            recommendations.append("Consider applying Single Responsibility Principle to classes")
        
        return recommendations
    
    def _identify_high_risk_functions(self, code: str, features: Dict[str, Any]) -> List[str]:
        """Identify potentially high-risk functions in the code."""
        high_risk_functions = []
        
        try:
            import ast
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Calculate function-specific metrics
                    func_lines = node.end_lineno - node.lineno + 1 if hasattr(node, 'end_lineno') else 0
                    func_complexity = self._calculate_function_complexity(node)
                    func_nesting = self._calculate_function_nesting(node)
                    
                    # Flag high-risk functions
                    risk_factors = []
                    if func_lines > 50:
                        risk_factors.append("long")
                    if func_complexity > 10:
                        risk_factors.append("complex")
                    if func_nesting > 3:
                        risk_factors.append("deeply nested")
                    
                    if risk_factors:
                        high_risk_functions.append(f"{node.name} ({', '.join(risk_factors)})")
        
        except Exception as e:
            logger.warning(f"Could not analyze functions: {e}")
        
        return high_risk_functions[:5]  # Return top 5 high-risk functions
    
    def _calculate_function_complexity(self, func_node) -> int:
        """Calculate cyclomatic complexity for a specific function."""
        complexity = 1  # Base complexity
        
        for node in ast.walk(func_node):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.With)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        
        return complexity
    
    def _calculate_function_nesting(self, func_node) -> int:
        """Calculate maximum nesting depth for a specific function."""
        max_depth = 0
        
        def get_depth(node, current_depth=0):
            nonlocal max_depth
            max_depth = max(max_depth, current_depth)
            
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.If, ast.While, ast.For, ast.With, ast.Try)):
                    get_depth(child, current_depth + 1)
                else:
                    get_depth(child, current_depth)
        
        get_depth(func_node)
        return max_depth
    
    def _get_prediction_confidence(self, risk_score: float) -> str:
        """Get confidence level based on prediction score."""
        if risk_score > 0.8 or risk_score < 0.2:
            return "High"
        elif risk_score > 0.6 or risk_score < 0.4:
            return "Medium"
        else:
            return "Low"
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model."""
        if not self.model_loaded or self.model is None:
            return {"status": "Model not loaded"}
        
        info = {
            "status": "Model loaded",
            "model_type": type(self.model).__name__,
            "features": self.feature_names
        }
        
        if hasattr(self.model, 'n_estimators'):
            info["n_estimators"] = self.model.n_estimators
        
        if hasattr(self.model, 'max_depth'):
            info["max_depth"] = self.model.max_depth
        
        if hasattr(self.model, 'feature_importances_'):
            info["feature_importances_available"] = True
        
        return info
