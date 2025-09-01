import base64
import io
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

class ChartGenerator:
    @staticmethod
    def create_time_distribution_chart(data):
        """Create a pie chart for time distribution"""
        labels = [item['_id'].capitalize() for item in data]
        sizes = [item['total_hours'] for item in data]
        
        plt.figure(figsize=(8, 8))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        plt.title('Time Distribution by Category')
        
        # Save to buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plt.close()
        
        return base64.b64encode(buf.getvalue()).decode('utf-8')
    
    @staticmethod
    def create_productivity_trend_chart(trends):
        """Create a line chart for productivity trends"""
        dates = [datetime.strptime(t['date'], '%Y-%m-%d') for t in trends]
        hours = [t['productive_hours'] for t in trends]
        day_names = [t['day_name'] for t in trends]
        
        plt.figure(figsize=(10, 6))
        plt.plot(dates, hours, marker='o', linewidth=2, markersize=8)
        plt.fill_between(dates, hours, alpha=0.3)
        
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator())
        plt.gcf().autofmt_xdate()
        
        plt.title('Productivity Trends (Last 7 Days)')
        plt.ylabel('Productive Hours')
        plt.grid(True, alpha=0.3)
        
        # Add day names as labels
        for i, (date, hour, day) in enumerate(zip(dates, hours, day_names)):
            plt.annotate(day, (date, hour), textcoords="offset points", 
                        xytext=(0,10), ha='center', fontsize=8)
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plt.close()
        
        return base64.b64encode(buf.getvalue()).decode('utf-8')
    
    @staticmethod
    def create_peak_hours_chart(peak_hours):
        """Create a bar chart for peak hours"""
        hours = [f"{h:02d}:00" for h in range(24)]
        values = [data['hours'] for data in peak_hours]
        
        plt.figure(figsize=(12, 6))
        bars = plt.bar(hours, values, alpha=0.7)
        
        # Color the bars based on value - handle division by zero
        max_val = max(values) if values else 1
        
        # Use a safe division that returns 0 when dividing by 0
        for bar, val in zip(bars, values):
            normalized_val = val / max_val if max_val > 0 else 0
            bar.set_alpha(0.3 + 0.7 * normalized_val)
            bar.set_color(plt.cm.viridis(normalized_val))
        
        plt.title('Peak Productivity Hours')
        plt.xlabel('Hour of Day')
        plt.ylabel('Total Work Hours')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plt.close()
        
        return base64.b64encode(buf.getvalue()).decode('utf-8')