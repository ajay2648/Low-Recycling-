import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json

class ConstructionWasteAnalyzer:
    """Analyzes construction waste recycling rates and patterns"""
    
    def __init__(self):
        self.waste_data = None
        self.recycling_targets = {
            'concrete': 0.85,
            'metal': 0.90,
            'wood': 0.70,
            'plastic': 0.60,
            'mixed': 0.50
        }
    
    def generate_sample_data(self, num_projects=50):
        """Generate sample construction waste data"""
        np.random.seed(42)
        
        waste_types = ['concrete', 'metal', 'wood', 'plastic', 'mixed']
        project_ids = [f'PRJ-{i:03d}' for i in range(1, num_projects + 1)]
        
        data = []
        start_date = datetime(2024, 1, 1)
        
        for project_id in project_ids:
            project_date = start_date + timedelta(days=np.random.randint(0, 300))
            
            for waste_type in waste_types:
                total_waste = np.random.uniform(500, 5000)
                
                # Current recycling rates are low (20-60%)
                current_rate = np.random.uniform(0.20, 0.60)
                recycled_waste = total_waste * current_rate
                
                data.append({
                    'project_id': project_id,
                    'date': project_date,
                    'waste_type': waste_type,
                    'total_waste_kg': round(total_waste, 2),
                    'recycled_kg': round(recycled_waste, 2),
                    'recycling_rate': round(current_rate, 3),
                    'location': np.random.choice(['Urban', 'Suburban', 'Rural']),
                    'project_type': np.random.choice(['Residential', 'Commercial', 'Industrial'])
                })
        
        self.waste_data = pd.DataFrame(data)
        return self.waste_data
    
    def calculate_statistics(self):
        """Calculate key recycling statistics"""
        if self.waste_data is None:
            print("No data available. Generate data first.")
            return
        
        stats = {
            'overall_recycling_rate': self.waste_data['recycled_kg'].sum() / 
                                     self.waste_data['total_waste_kg'].sum(),
            'total_waste_generated': self.waste_data['total_waste_kg'].sum(),
            'total_waste_recycled': self.waste_data['recycled_kg'].sum(),
            'waste_by_type': self.waste_data.groupby('waste_type').agg({
                'total_waste_kg': 'sum',
                'recycled_kg': 'sum',
                'recycling_rate': 'mean'
            }).to_dict(),
            'by_location': self.waste_data.groupby('location')['recycling_rate'].mean().to_dict(),
            'by_project_type': self.waste_data.groupby('project_type')['recycling_rate'].mean().to_dict()
        }
        
        return stats
    
    def identify_improvement_opportunities(self):
        """Identify areas with low recycling rates"""
        if self.waste_data is None:
            return
        
        opportunities = []
        
        for waste_type, target_rate in self.recycling_targets.items():
            current_rate = self.waste_data[self.waste_data['waste_type'] == waste_type]['recycling_rate'].mean()
            gap = target_rate - current_rate
            
            if gap > 0:
                potential_increase = self.waste_data[
                    self.waste_data['waste_type'] == waste_type
                ]['total_waste_kg'].sum() * gap
                
                opportunities.append({
                    'waste_type': waste_type,
                    'current_rate': round(current_rate, 3),
                    'target_rate': target_rate,
                    'gap': round(gap, 3),
                    'potential_additional_recycling_kg': round(potential_increase, 2)
                })
        
        return pd.DataFrame(opportunities).sort_values('potential_additional_recycling_kg', ascending=False)
    
    def visualize_recycling_rates(self):
        """Create visualizations for recycling analysis"""
        if self.waste_data is None:
            print("No data available.")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Recycling rate by waste type
        waste_type_avg = self.waste_data.groupby('waste_type')['recycling_rate'].mean().sort_values()
        targets = [self.recycling_targets[wt] for wt in waste_type_avg.index]
        
        x = np.arange(len(waste_type_avg))
        width = 0.35
        
        axes[0, 0].bar(x - width/2, waste_type_avg.values, width, label='Current Rate', color='coral')
        axes[0, 0].bar(x + width/2, targets, width, label='Target Rate', color='lightgreen')
        axes[0, 0].set_xlabel('Waste Type')
        axes[0, 0].set_ylabel('Recycling Rate')
        axes[0, 0].set_title('Current vs Target Recycling Rates by Waste Type')
        axes[0, 0].set_xticks(x)
        axes[0, 0].set_xticklabels(waste_type_avg.index, rotation=45)
        axes[0, 0].legend()
        axes[0, 0].grid(axis='y', alpha=0.3)
        
        # 2. Total waste vs recycled waste
        waste_summary = self.waste_data.groupby('waste_type').agg({
            'total_waste_kg': 'sum',
            'recycled_kg': 'sum'
        })
        
        waste_summary.plot(kind='bar', ax=axes[0, 1], color=['#ff6b6b', '#51cf66'])
        axes[0, 1].set_title('Total Waste Generated vs Recycled by Type')
        axes[0, 1].set_xlabel('Waste Type')
        axes[0, 1].set_ylabel('Weight (kg)')
        axes[0, 1].legend(['Total Waste', 'Recycled'])
        axes[0, 1].tick_params(axis='x', rotation=45)
        axes[0, 1].grid(axis='y', alpha=0.3)
        
        # 3. Recycling rate by location
        location_data = self.waste_data.groupby('location')['recycling_rate'].mean().sort_values()
        axes[1, 0].barh(location_data.index, location_data.values, color='skyblue')
        axes[1, 0].set_xlabel('Average Recycling Rate')
        axes[1, 0].set_title('Recycling Rates by Location')
        axes[1, 0].grid(axis='x', alpha=0.3)
        
        # 4. Recycling rate by project type
        project_data = self.waste_data.groupby('project_type')['recycling_rate'].mean().sort_values()
        axes[1, 1].barh(project_data.index, project_data.values, color='plum')
        axes[1, 1].set_xlabel('Average Recycling Rate')
        axes[1, 1].set_title('Recycling Rates by Project Type')
        axes[1, 1].grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('construction_waste_analysis.png', dpi=300, bbox_inches='tight')
        print("Visualization saved as 'construction_waste_analysis.png'")
        plt.show()
    
    def generate_recommendations(self):
        """Generate recommendations to improve recycling rates"""
        recommendations = [
            {
                'category': 'Infrastructure',
                'recommendations': [
                    'Establish on-site waste sorting facilities',
                    'Partner with specialized recycling centers',
                    'Install waste compactors to reduce transport costs'
                ]
            },
            {
                'category': 'Training & Awareness',
                'recommendations': [
                    'Conduct regular training for construction workers on waste segregation',
                    'Display visual guides for proper waste sorting',
                    'Implement incentive programs for projects with high recycling rates'
                ]
            },
            {
                'category': 'Policy & Planning',
                'recommendations': [
                    'Mandate waste management plans before project approval',
                    'Set minimum recycling rate requirements in building codes',
                    'Provide tax incentives for using recycled construction materials'
                ]
            },
            {
                'category': 'Technology',
                'recommendations': [
                    'Use digital tracking systems for waste streams',
                    'Implement AI-based sorting technologies',
                    'Adopt Building Information Modeling (BIM) for waste reduction'
                ]
            }
        ]
        return recommendations


class WasteManagementSystem:
    """System to track and manage construction waste recycling"""
    
    def __init__(self):
        self.projects = {}
    
    def add_project(self, project_id, project_name, location, project_type):
        """Add a new construction project"""
        self.projects[project_id] = {
            'name': project_name,
            'location': location,
            'project_type': project_type,
            'waste_entries': [],
            'created_at': datetime.now().isoformat()
        }
        print(f"Project {project_id} - {project_name} added successfully!")
    
    def log_waste(self, project_id, waste_type, total_kg, recycled_kg):
        """Log waste generation and recycling"""
        if project_id not in self.projects:
            print(f"Project {project_id} not found!")
            return
        
        entry = {
            'date': datetime.now().isoformat(),
            'waste_type': waste_type,
            'total_kg': total_kg,
            'recycled_kg': recycled_kg,
            'recycling_rate': recycled_kg / total_kg if total_kg > 0 else 0
        }
        
        self.projects[project_id]['waste_entries'].append(entry)
        print(f"Waste entry logged for project {project_id}")
    
    def get_project_summary(self, project_id):
        """Get waste summary for a specific project"""
        if project_id not in self.projects:
            print(f"Project {project_id} not found!")
            return
        
        project = self.projects[project_id]
        entries = project['waste_entries']
        
        if not entries:
            print(f"No waste entries for project {project_id}")
            return
        
        total_waste = sum(e['total_kg'] for e in entries)
        total_recycled = sum(e['recycled_kg'] for e in entries)
        
        summary = {
            'project_name': project['name'],
            'location': project['location'],
            'project_type': project['project_type'],
            'total_waste_kg': total_waste,
            'total_recycled_kg': total_recycled,
            'overall_recycling_rate': total_recycled / total_waste if total_waste > 0 else 0,
            'entries_count': len(entries)
        }
        
        return summary
    
    def export_data(self, filename='waste_data.json'):
        """Export all data to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.projects, f, indent=2)
        print(f"Data exported to {filename}")



if __name__ == "__main__":
    print("=" * 70)
    print("CONSTRUCTION WASTE RECYCLING ANALYSIS SYSTEM")
    print("=" * 70)
    
    
    analyzer = ConstructionWasteAnalyzer()
    
    
    print("\n1. Generating sample construction waste data...")
    df = analyzer.generate_sample_data(num_projects=50)
    print(f"Generated data for {len(df)} waste entries across 50 projects")
    print("\nSample data:")
    print(df.head(10))
    
    
    print("\n" + "=" * 70)
    print("2. RECYCLING STATISTICS")
    print("=" * 70)
    stats = analyzer.calculate_statistics()
    print(f"\nOverall Recycling Rate: {stats['overall_recycling_rate']:.2%}")
    print(f"Total Waste Generated: {stats['total_waste_generated']:,.2f} kg")
    print(f"Total Waste Recycled: {stats['total_waste_recycled']:,.2f} kg")
    
    print("\n--- Recycling Rates by Waste Type ---")
    for waste_type, data in stats['waste_by_type']['recycling_rate'].items():
        print(f"{waste_type.capitalize()}: {data:.2%}")
    
    
    print("\n" + "=" * 70)
    print("3. IMPROVEMENT OPPORTUNITIES")
    print("=" * 70)
    opportunities = analyzer.identify_improvement_opportunities()
    print(opportunities.to_string(index=False))
    
    
    print("\n" + "=" * 70)
    print("4. RECOMMENDATIONS TO IMPROVE RECYCLING RATES")
    print("=" * 70)
    recommendations = analyzer.generate_recommendations()
    for rec in recommendations:
        print(f"\n{rec['category']}:")
        for i, item in enumerate(rec['recommendations'], 1):
            print(f"  {i}. {item}")
    
    
    print("\n" + "=" * 70)
    print("5. GENERATING VISUALIZATIONS")
    print("=" * 70)
    analyzer.visualize_recycling_rates()
    
    
    print("\n" + "=" * 70)
    print("6. WASTE MANAGEMENT SYSTEM DEMO")
    print("=" * 70)
    
    wms = WasteManagementSystem()
    wms.add_project('PRJ-001', 'Green Tower Construction', 'Urban', 'Commercial')
    wms.log_waste('PRJ-001', 'concrete', 1500, 900)
    wms.log_waste('PRJ-001', 'metal', 500, 400)
    wms.log_waste('PRJ-001', 'wood', 800, 480)
    
    print("\nProject Summary:")
    summary = wms.get_project_summary('PRJ-001')
    for key, value in summary.items():
        if isinstance(value, float):
            if 'rate' in key:
                print(f"{key}: {value:.2%}")
            else:
                print(f"{key}: {value:,.2f}")
        else:
            print(f"{key}: {value}")
    
    print("\n" + "=" * 70)
    print("Analysis Complete!")
    print("=" * 70)