"""
Database Decision Engine
Core logic for comparing MySQL, PostgreSQL, and MongoDB
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class DatabaseProfile:
    """Data class representing a database profile"""
    name: str
    db_type: str
    score: int
    pros: List[str]
    cons: List[str]


@dataclass
class Tradeoff:
    """Data class representing a trade-off"""
    title: str
    description: str


@dataclass
class Alternative:
    """Data class representing an alternative database"""
    database: str
    reason: str


@dataclass
class Recommendation:
    """Data class representing the final recommendation"""
    database: str
    confidence: str
    reasoning: List[str]


class DecisionEngine:
    """
    Rule-based decision engine for database selection.
    Uses weighted scoring system based on user requirements.
    """
    
    def __init__(self):
        self.databases = ['mysql', 'postgresql', 'mongodb']
        self._initialize_scoring_rules()
        self._initialize_database_profiles()
    
    def _initialize_scoring_rules(self):
        """Initialize scoring rules for each criterion"""
        
        # Application Type Scoring (max 4 points)
        self.app_type_scores = {
            'Web': {'mysql': 3, 'postgresql': 3, 'mongodb': 2},
            'Analytics': {'mysql': 2, 'postgresql': 4, 'mongodb': 1},
            'Real-time': {'mysql': 2, 'postgresql': 2, 'mongodb': 4}
        }
        
        # Data Structure Scoring (max 4 points)
        self.data_structure_scores = {
            'Structured': {'mysql': 4, 'postgresql': 4, 'mongodb': 1},
            'Semi-structured': {'mysql': 2, 'postgresql': 3, 'mongodb': 4},
            'Unstructured': {'mysql': 1, 'postgresql': 2, 'mongodb': 4}
        }
        
        # Scalability Scoring (max 4 points)
        self.scalability_scores = {
            'Low': {'mysql': 3, 'postgresql': 3, 'mongodb': 2},
            'Medium': {'mysql': 3, 'postgresql': 3, 'mongodb': 3},
            'High': {'mysql': 2, 'postgresql': 2, 'mongodb': 4}
        }
        
        # Transaction Scoring (max 4 points)
        self.transaction_scores = {
            'Low': {'mysql': 2, 'postgresql': 2, 'mongodb': 3},
            'High': {'mysql': 4, 'postgresql': 4, 'mongodb': 2}
        }
        
        # Schema Flexibility Scoring (max 4 points)
        self.schema_scores = {
            'Yes': {'mysql': 1, 'postgresql': 2, 'mongodb': 4},
            'No': {'mysql': 4, 'postgresql': 4, 'mongodb': 2}
        }
    
    def _initialize_database_profiles(self):
        """Initialize static database profiles with pros and cons"""
        
        self.db_profiles = {
            'mysql': {
                'name': 'MySQL',
                'type': 'Relational (SQL)',
                'pros': [
                    'Mature and widely adopted with extensive community support',
                    'Excellent for structured data with ACID compliance',
                    'Strong performance for read-heavy workloads',
                    'Easy to learn and widely supported by hosting providers',
                    'Great for traditional web applications'
                ],
                'cons': [
                    'Limited support for complex analytics queries',
                    'Horizontal scaling requires additional complexity (sharding)',
                    'Less flexible with schema changes',
                    'JSON support is basic compared to PostgreSQL',
                    'Advanced features lag behind PostgreSQL'
                ]
            },
            'postgresql': {
                'name': 'PostgreSQL',
                'type': 'Relational (SQL)',
                'pros': [
                    'Most advanced open-source relational database',
                    'Excellent for complex queries and analytics',
                    'Superior JSON/JSONB support for semi-structured data',
                    'Strong extensibility with custom functions and data types',
                    'Best-in-class data integrity and ACID compliance'
                ],
                'cons': [
                    'Slightly steeper learning curve than MySQL',
                    'Higher memory consumption',
                    'Horizontal scaling still requires effort',
                    'Can be overkill for simple applications',
                    'Configuration complexity for optimization'
                ]
            },
            'mongodb': {
                'name': 'MongoDB',
                'type': 'NoSQL (Document)',
                'pros': [
                    'Excellent horizontal scalability (built-in sharding)',
                    'Schema flexibility for evolving data models',
                    'High performance for real-time applications',
                    'Natural fit for JSON/document-based data',
                    'Easy to get started with minimal setup'
                ],
                'cons': [
                    'Eventual consistency can complicate transactions',
                    'No built-in joins (requires application-level logic)',
                    'Higher storage overhead',
                    'Not ideal for complex relational data',
                    'ACID transactions only within single documents by default'
                ]
            }
        }
    
    def calculate_scores(self, user_inputs: Dict[str, str]) -> Dict[str, int]:
        """
        Calculate scores for each database based on user inputs.
        
        Args:
            user_inputs: Dictionary containing user selections
            
        Returns:
            Dictionary with database scores
        """
        scores = {db: 0 for db in self.databases}
        
        # Application Type
        if user_inputs['app_type'] in self.app_type_scores:
            for db in self.databases:
                scores[db] += self.app_type_scores[user_inputs['app_type']][db]
        
        # Data Structure
        if user_inputs['data_structure'] in self.data_structure_scores:
            for db in self.databases:
                scores[db] += self.data_structure_scores[user_inputs['data_structure']][db]
        
        # Scalability
        if user_inputs['scalability'] in self.scalability_scores:
            for db in self.databases:
                scores[db] += self.scalability_scores[user_inputs['scalability']][db]
        
        # Transactions
        if user_inputs['transactions'] in self.transaction_scores:
            for db in self.databases:
                scores[db] += self.transaction_scores[user_inputs['transactions']][db]
        
        # Schema Flexibility
        if user_inputs['schema_flexibility'] in self.schema_scores:
            for db in self.databases:
                scores[db] += self.schema_scores[user_inputs['schema_flexibility']][db]
        
        return scores
    
    def generate_database_profiles(self, scores: Dict[str, int]) -> List[DatabaseProfile]:
        """
        Generate database profiles with scores.
        
        Args:
            scores: Dictionary with database scores
            
        Returns:
            List of DatabaseProfile objects sorted by score
        """
        profiles = []
        
        for db_key in self.databases:
            profile = DatabaseProfile(
                name=self.db_profiles[db_key]['name'],
                db_type=self.db_profiles[db_key]['type'],
                score=scores[db_key],
                pros=self.db_profiles[db_key]['pros'],
                cons=self.db_profiles[db_key]['cons']
            )
            profiles.append(profile)
        
        # Sort by score in descending order
        profiles.sort(key=lambda x: x.score, reverse=True)
        
        return profiles
    
    def identify_tradeoffs(self, user_inputs: Dict[str, str]) -> List[Tradeoff]:
        """
        Identify relevant trade-offs based on user inputs.
        
        Args:
            user_inputs: Dictionary containing user selections
            
        Returns:
            List of Tradeoff objects
        """
        tradeoffs = []
        
        # Schema rigidity vs flexibility
        if (user_inputs['data_structure'] == 'Structured' and 
            user_inputs['schema_flexibility'] == 'Yes'):
            tradeoffs.append(Tradeoff(
                title='Schema Rigidity vs Flexibility',
                description='You want structured data but also schema flexibility. '
                           'SQL databases enforce schemas strongly, while MongoDB offers '
                           'flexibility but sacrifices relational integrity.'
            ))
        
        # Consistency vs scalability
        if (user_inputs['scalability'] == 'High' and 
            user_inputs['transactions'] == 'High'):
            tradeoffs.append(Tradeoff(
                title='Consistency vs Scalability (CAP Theorem)',
                description='High scalability often requires eventual consistency (MongoDB), '
                           'but high transaction requirements need strong ACID guarantees '
                           '(PostgreSQL/MySQL). This is a fundamental distributed systems trade-off.'
            ))
        
        # SQL vs NoSQL for analytics
        if (user_inputs['app_type'] == 'Analytics' and 
            user_inputs['scalability'] == 'High'):
            tradeoffs.append(Tradeoff(
                title='SQL vs NoSQL for Analytics',
                description='SQL databases excel at complex queries and joins, but NoSQL scales '
                           'better horizontally. Consider PostgreSQL with read replicas or '
                           'specialized analytics databases like ClickHouse.'
            ))
        
        # Document flexibility vs transaction integrity
        if (user_inputs['data_structure'] == 'Unstructured' and 
            user_inputs['transactions'] == 'High'):
            tradeoffs.append(Tradeoff(
                title='Document Flexibility vs Transaction Integrity',
                description='MongoDB handles unstructured data well but has limited multi-document '
                           'transaction support. PostgreSQL JSONB offers a middle ground with '
                           'strong transactions and flexible document storage.'
            ))
        
        # Read vs write optimization
        if user_inputs['app_type'] == 'Web':
            tradeoffs.append(Tradeoff(
                title='Read Optimization vs Write Optimization',
                description='MySQL excels at read-heavy workloads, MongoDB at write-heavy ones. '
                           'PostgreSQL balances both. Consider your read/write ratio.'
            ))
        
        return tradeoffs
    
    def generate_recommendation(self, profiles: List[DatabaseProfile], 
                               user_inputs: Dict[str, str]) -> Recommendation:
        """
        Generate final recommendation with reasoning.
        
        Args:
            profiles: List of DatabaseProfile objects (sorted by score)
            user_inputs: Dictionary containing user selections
            
        Returns:
            Recommendation object
        """
        top_db = profiles[0]
        reasoning = []
        
        # MySQL-specific reasoning
        if top_db.name == 'MySQL':
            reasoning.append('MySQL is recommended for your traditional web application needs '
                           'with structured data.')
            
            if user_inputs['transactions'] == 'High':
                reasoning.append('Strong ACID compliance meets your transaction requirements.')
            
            if user_inputs['scalability'] != 'High':
                reasoning.append('Vertical scaling is sufficient for your scalability needs.')
            
            if user_inputs['app_type'] == 'Web':
                reasoning.append('Proven track record for web applications with excellent '
                               'community support.')
        
        # PostgreSQL-specific reasoning
        elif top_db.name == 'PostgreSQL':
            reasoning.append('PostgreSQL offers the best balance of advanced features for '
                           'your requirements.')
            
            if user_inputs['app_type'] == 'Analytics':
                reasoning.append('Superior query optimization and window functions support '
                               'complex analytics workloads.')
            
            if user_inputs['data_structure'] == 'Semi-structured':
                reasoning.append('Excellent JSONB support handles semi-structured data efficiently '
                               'while maintaining relational integrity.')
            
            if user_inputs['transactions'] == 'High':
                reasoning.append('Industry-leading ACID compliance and advanced transaction '
                               'isolation ensures data integrity.')
            
            if user_inputs['schema_flexibility'] == 'Yes':
                reasoning.append('JSONB and extension support provide flexibility while maintaining '
                               'SQL capabilities.')
        
        # MongoDB-specific reasoning
        else:  # MongoDB
            reasoning.append('MongoDB is the best choice for your scalability and flexibility needs.')
            
            if user_inputs['scalability'] == 'High':
                reasoning.append('Built-in sharding provides excellent horizontal scalability '
                               'without complex configuration.')
            
            if user_inputs['schema_flexibility'] == 'Yes':
                reasoning.append('Schema-less design allows rapid iteration and accommodates '
                               'evolving data models.')
            
            if user_inputs['app_type'] == 'Real-time':
                reasoning.append('Optimized for high-throughput real-time applications with '
                               'low-latency operations.')
            
            if user_inputs['data_structure'] == 'Unstructured':
                reasoning.append('Document model naturally fits unstructured and hierarchical data.')
        
        # Add close competition note
        if len(profiles) > 1:
            score_diff = profiles[0].score - profiles[1].score
            if score_diff <= 2:
                reasoning.append(f'Note: {profiles[1].name} scored closely '
                               f'({profiles[1].score} vs {profiles[0].score}). '
                               f'Consider evaluating both options based on team expertise.')
        
        # Determine confidence level
        score_diff = profiles[0].score - profiles[1].score if len(profiles) > 1 else 5
        if score_diff > 3:
            confidence = 'High'
        elif score_diff > 1:
            confidence = 'Medium'
        else:
            confidence = 'Low'
        
        return Recommendation(
            database=top_db.name,
            confidence=confidence,
            reasoning=reasoning
        )
    
    def suggest_alternatives(self, user_inputs: Dict[str, str]) -> List[Alternative]:
        """
        Suggest alternative databases for specific use cases.
        
        Args:
            user_inputs: Dictionary containing user selections
            
        Returns:
            List of Alternative objects
        """
        alternatives = []
        
        # Analytics + High Scalability
        if (user_inputs['app_type'] == 'Analytics' and 
            user_inputs['scalability'] == 'High'):
            alternatives.append(Alternative(
                database='ClickHouse or Apache Druid',
                reason='Columnar databases optimized for massive-scale analytics and '
                       'OLAP queries with superior compression and query performance.'
            ))
        
        # Real-time + Unstructured
        if (user_inputs['app_type'] == 'Real-time' and 
            user_inputs['data_structure'] == 'Unstructured'):
            alternatives.append(Alternative(
                database='Redis or Apache Kafka',
                reason='In-memory data stores and streaming platforms optimized for '
                       'real-time data processing and sub-millisecond latency.'
            ))
        
        # High scalability + High transactions
        if (user_inputs['scalability'] == 'High' and 
            user_inputs['transactions'] == 'High'):
            alternatives.append(Alternative(
                database='CockroachDB or Google Spanner',
                reason='Distributed SQL databases offering both horizontal scalability and '
                       'strong consistency (bypassing CAP theorem limitations).'
            ))
        
        # Unstructured + Analytics
        if (user_inputs['data_structure'] == 'Unstructured' and 
            user_inputs['app_type'] == 'Analytics'):
            alternatives.append(Alternative(
                database='Elasticsearch',
                reason='Excellent for full-text search, log analytics, and unstructured '
                       'data exploration with powerful aggregation capabilities.'
            ))
        
        # Time-series workloads
        if user_inputs['app_type'] == 'Real-time':
            alternatives.append(Alternative(
                database='TimescaleDB or InfluxDB',
                reason='Specialized time-series databases for IoT, monitoring, and '
                       'event-driven applications requiring time-based queries.'
            ))
        
        return alternatives
    
    def analyze(self, user_inputs: Dict[str, str]) -> Dict:
        """
        Main analysis method - orchestrates the entire decision process.
        
        Args:
            user_inputs: Dictionary containing user selections
            
        Returns:
            Dictionary containing complete analysis results
        """
        # Calculate scores
        scores = self.calculate_scores(user_inputs)
        
        # Generate database profiles
        profiles = self.generate_database_profiles(scores)
        
        # Identify trade-offs
        tradeoffs = self.identify_tradeoffs(user_inputs)
        
        # Generate recommendation
        recommendation = self.generate_recommendation(profiles, user_inputs)
        
        # Suggest alternatives
        alternatives = self.suggest_alternatives(user_inputs)
        
        return {
            'profiles': profiles,
            'tradeoffs': tradeoffs,
            'recommendation': recommendation,
            'alternatives': alternatives,
            'scores': scores
        }


# Example usage
if __name__ == '__main__':
    engine = DecisionEngine()
    
    # Example user inputs
    test_inputs = {
        'app_type': 'Analytics',
        'data_structure': 'Semi-structured',
        'scalability': 'High',
        'transactions': 'High',
        'schema_flexibility': 'Yes'
    }
    
    results = engine.analyze(test_inputs)
    
    print("=== RECOMMENDATION ===")
    print(f"Database: {results['recommendation'].database}")
    print(f"Confidence: {results['recommendation'].confidence}")
    print("\nReasoning:")
    for reason in results['recommendation'].reasoning:
        print(f"  • {reason}")
    
    print("\n=== DATABASE COMPARISON ===")
    for profile in results['profiles']:
        print(f"\n{profile.name} (Score: {profile.score})")
        print(f"Type: {profile.db_type}")
    
    print("\n=== TRADE-OFFS ===")
    for tradeoff in results['tradeoffs']:
        print(f"\n{tradeoff.title}")
        print(f"  {tradeoff.description}")
