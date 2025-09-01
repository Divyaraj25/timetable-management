from datetime import datetime, timedelta
from collections import defaultdict
from flask_pymongo import PyMongo
import statistics

class TimeAnalytics:
    def __init__(self, mongo):
        self.mongo = mongo
    
    def get_time_distribution(self, user_id, days=30):
        """Get time distribution by event type for the specified period"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        pipeline = [
            {
                '$match': {
                    'user_id': user_id,
                    'start_time': {'$gte': start_date, '$lte': end_date}
                }
            },
            {
                '$group': {
                    '_id': '$event_type',
                    'total_hours': {'$sum': {
                        '$divide': [
                            {'$subtract': ['$end_time', '$start_time']},
                            3600000  # Convert milliseconds to hours
                        ]
                    }},
                    'event_count': {'$sum': 1}
                }
            },
            {
                '$sort': {'total_hours': -1}
            }
        ]
        
        results = list(self.mongo.db.events.aggregate(pipeline))
        return results
    
    def get_productivity_trends(self, user_id, days=7):
        """Get daily productivity trends"""
        trends = []
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            start_of_day = datetime.combine(date, datetime.min.time())
            end_of_day = datetime.combine(date, datetime.max.time())
            
            productive_events = list(self.mongo.db.events.find({
                'user_id': user_id,
                'start_time': {'$gte': start_of_day, '$lte': end_of_day},
                'event_type': {'$in': ['work', 'health', 'learning']}
            }))
            
            productive_hours = sum(
                (event['end_time'] - event['start_time']).total_seconds() / 3600
                for event in productive_events
            )
            
            trends.append({
                'date': date.strftime('%Y-%m-%d'),
                'productive_hours': round(productive_hours, 2),
                'day_name': date.strftime('%A')
            })
        
        return list(reversed(trends))
    
    def get_peak_hours(self, user_id, days=30):
        """Identify peak productivity hours"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        events = list(self.mongo.db.events.find({
            'user_id': user_id,
            'start_time': {'$gte': start_date, '$lte': end_date},
            'event_type': 'work'
        }))
        
        hour_distribution = defaultdict(int)
        for event in events:
            hour = event['start_time'].hour
            duration = (event['end_time'] - event['start_time']).total_seconds() / 3600
            hour_distribution[hour] += duration
        
        # Convert to list and sort
        peak_hours = [{'hour': h, 'hours': hour_distribution[h]} for h in range(24)]
        return peak_hours
    
    def get_category_efficiency(self, user_id):
        """Calculate efficiency metrics by category"""
        categories = ['work', 'personal', 'health', 'other']
        efficiency_data = []
        
        for category in categories:
            events = list(self.mongo.db.events.find({
                'user_id': user_id,
                'event_type': category
            }))
            
            if events:
                avg_duration = statistics.mean(
                    (e['end_time'] - e['start_time']).total_seconds() / 3600 
                    for e in events
                )
                total_events = len(events)
                efficiency_data.append({
                    'category': category,
                    'avg_duration': round(avg_duration, 2),
                    'total_events': total_events
                })
        
        return efficiency_data