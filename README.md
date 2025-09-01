# Timetable Management System

A comprehensive web-based timetable management system built with Flask and MongoDB, designed to help users efficiently organize and manage their schedules, events, and tasks.

## Features

- 🗓️ **Daily, Weekly, Monthly, and Yearly Views** - Visualize your schedule in different time frames
- 🔔 **Event Notifications** - Email notifications for upcoming events
- 📊 **Analytics Dashboard** - Track how you spend your time with visual analytics
- 📱 **Responsive Design** - Access your schedule from any device
- 🔄 **Recurring Events** - Set up events that repeat daily, weekly, monthly, or yearly
- 📧 **Email Integration** - Receive email reminders for important events
- 📈 **Productivity Tracking** - Monitor your productivity trends over time

## Tech Stack

- **Backend**: Python 3.13, Flask
- **Database**: MongoDB
- **Frontend**: HTML5, CSS3, JavaScript
- **Data Visualization**: Matplotlib
- **Email**: Flask-Mail

## Prerequisites

- Python 3.13 or higher
- MongoDB server
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd timetable-management_working
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root with the following variables:
   ```
   SECRET_KEY=your-secret-key
   MONGO_URI=mongodb://localhost:27017/timetable_db
   MAIL_SERVER=smtp.example.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-email@example.com
   MAIL_PASSWORD=your-email-password
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open your web browser and navigate to `http://localhost:5000`

## Usage

### Creating Events
1. Click on the "New Event" button
2. Fill in the event details (title, description, date, time, duration)
3. Set recurrence if needed
4. Click "Save"

### Viewing Your Schedule
- Use the navigation bar to switch between different views (Day, Week, Month, Year)
- Click on any event to view or edit its details

### Analytics Dashboard
- Access the analytics section to view:
  - Time distribution by category
  - Productivity trends
  - Event statistics

## Benefits

### For Individuals
- **Better Time Management**: Visualize and optimize your daily schedule
- **Increased Productivity**: Track how you spend your time and identify areas for improvement
- **Never Miss Important Events**: Get email reminders for upcoming events
- **Data-Driven Decisions**: Use analytics to understand your time allocation patterns

### For Teams/Organizations
- **Centralized Scheduling**: Manage team events and meetings in one place
- **Improved Coordination**: Share availability and schedule meetings efficiently
- **Resource Planning**: Allocate resources based on scheduled events

## Advanced Features

### Email Notifications
- Customize notification preferences
- Set reminders for specific events
- Receive daily agenda emails

### Data Export
- Export your schedule in various formats (CSV, iCal)
- Generate reports for specific time periods

### Integration
- Google Calendar sync (coming soon)
- Mobile app (coming soon)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue in the GitHub repository or contact the project maintainers.

---

**Happy Scheduling!** 🎉
