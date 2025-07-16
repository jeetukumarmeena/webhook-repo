# from flask import Blueprint, request, jsonify, render_template
# from app.extensions import mongo
# from datetime import datetime
# from zoneinfo import ZoneInfo 
# import json
# import pytz
# webhook_bp = Blueprint('webhook', __name__)
# ui_bp = Blueprint('ui', __name__)

# @webhook_bp.route('/webhook/receiver', methods=['POST'])
# def webhook_receiver():
#     try:
#         # Get the GitHub event type from headers
#         event_type = request.headers.get('X-GitHub-Event')
#         payload = request.get_json()
        
#         if not payload:
#             return jsonify({'error': 'No payload received'}), 400
        
#         # Process different event types
#         event_data = None
        
#         if event_type == 'push':
#             event_data = process_push_event(payload)
#         elif event_type == 'pull_request':
#             event_data = process_pull_request_event(payload)
#         elif event_type == 'merge':
#             event_data = process_merge_event(payload)
        
#         if event_data:
#             # Store in MongoDB
#             mongo.insert_event(event_data)
#             return jsonify({'status': 'success', 'message': 'Event processed successfully'}), 200
#         else:
#             return jsonify({'status': 'ignored', 'message': 'Event type not handled'}), 200
            
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# def process_push_event(payload):
#     try:
#         author = payload['pusher']['name']
#         to_branch = payload['ref'].split('/')[-1]  # Extract branch name from refs/heads/branch_name

#         ist = pytz.timezone('Asia/Kolkata')
#         timestamp = datetime.now(pytz.utc).astimezone(ist)

        
#         return {
#             'action': 'PUSH',
#             'author': author,
#             'to_branch': to_branch,
#             'from_branch': None,
#             'timestamp': timestamp,
#             'formatted_message': f'"{author}" pushed to "{to_branch}" on {timestamp.strftime("%d %B %Y - %I:%M %p UTC")}'
#         }
#     except KeyError as e:
#         print(f"Error processing push event: {e}")
#         return None

# def process_pull_request_event(payload):
#     try:
#         # Only process when PR is opened
#         if payload['action'] != 'opened':
#             return None
            
#         author = payload['pull_request']['user']['login']
#         from_branch = payload['pull_request']['head']['ref']
#         to_branch = payload['pull_request']['base']['ref']

#         ist = pytz.timezone('Asia/Kolkata')
#         timestamp = datetime.now(pytz.utc).astimezone(ist)
        
#         return {
#             'action': 'PULL_REQUEST',
#             'author': author,
#             'from_branch': from_branch,
#             'to_branch': to_branch,
#             'timestamp': timestamp,
#             'formatted_message': f'"{author}" submitted a pull request from "{from_branch}" to "{to_branch}" on {timestamp.strftime("%d %B %Y - %I:%M %p UTC")}'
#         }
#     except KeyError as e:
#         print(f"Error processing pull request event: {e}")
#         return None

# def process_merge_event(payload):
#     try:
#         # This would be triggered by a pull_request event with action 'closed' and merged = true
#         if payload.get('action') != 'closed' or not payload.get('pull_request', {}).get('merged'):
#             return None
            
#         author = payload['pull_request']['merged_by']['login']
#         from_branch = payload['pull_request']['head']['ref']
#         to_branch = payload['pull_request']['base']['ref']

#         ist = pytz.timezone('Asia/Kolkata')
#         timestamp = datetime.now(pytz.utc).astimezone(ist)
        
#         return {
#             'action': 'MERGE',
#             'author': author,
#             'from_branch': from_branch,
#             'to_branch': to_branch,
#             'timestamp': timestamp,
#             'formatted_message': f'"{author}" merged branch "{from_branch}" to "{to_branch}" on {timestamp.strftime("%d %B %Y - %I:%M %p UTC")}'
#         }
#     except KeyError as e:
#         print(f"Error processing merge event: {e}")
#         return None


# @ui_bp.route('/')
# def index():
#     """Render the main dashboard page"""
#     try:
#         return render_template('index.html')
#     except Exception as e:
#         print(f"Error rendering template: {e}")
#         return f"""
#         <html>
#         <head><title>GitHub Webhook Events</title></head>
#         <body>
#             <h1>GitHub Webhook Events Dashboard</h1>
#             <p>Error loading template: {str(e)}</p>
#             <p>Please check if templates/index.html exists in the app directory.</p>
#             <p><a href="/api/events">View Raw Events JSON</a></p>
#         </body>
#         </html>
#         """, 500



# @ui_bp.route('/api/events')
# def get_events():
#     try:
#         events = mongo.get_latest_events()
#         # Convert ObjectId to string for JSON serialization
#         for event in events:
#             if '_id' in event:
#                 event['_id'] = str(event['_id'])
#             # Convert datetime to string
#             if 'timestamp' in event:
#                 event['timestamp'] = event['timestamp'].isoformat()
        
#         return jsonify({
#             'events': events,
#             'total_count': mongo.get_event_count(),
#             'status': 'success'
#         })
#     except Exception as e:
#         print(f"Error in get_events: {e}")
#         return jsonify({'error': str(e), 'status': 'error'}), 500


from flask import Blueprint, request, jsonify, render_template
from app.extensions import mongo
from datetime import datetime
from zoneinfo import ZoneInfo 
import json
import pytz
webhook_bp = Blueprint('webhook', __name__)
ui_bp = Blueprint('ui', __name__)

@webhook_bp.route('/webhook/receiver', methods=['POST'])
def webhook_receiver():
    try:
        # Get the GitHub event type from headers
        event_type = request.headers.get('X-GitHub-Event')
        payload = request.get_json()
        
        if not payload:
            return jsonify({'error': 'No payload received'}), 400
        
        # Process different event types
        event_data = None
        
        if event_type == 'push':
            event_data = process_push_event(payload)
        elif event_type == 'pull_request':
            # Handle both PR opened and PR merged within the same event type
            if payload.get('action') == 'opened':
                event_data = process_pull_request_event(payload)
            elif payload.get('action') == 'closed' and payload.get('pull_request', {}).get('merged'):
                event_data = process_merge_event(payload)
        
        if event_data:
            # Store in MongoDB
            mongo.insert_event(event_data)
            return jsonify({'status': 'success', 'message': 'Event processed successfully'}), 200
        else:
            return jsonify({'status': 'ignored', 'message': 'Event type not handled'}), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def process_push_event(payload):
    try:
        author = payload['pusher']['name']
        to_branch = payload['ref'].split('/')[-1]  # Extract branch name from refs/heads/branch_name

        # Check if this is a merge commit by looking at the commit message
        commits = payload.get('commits', [])
        if commits:
            latest_commit = commits[-1]
            commit_message = latest_commit.get('message', '').lower()
            
            # Skip if this looks like a merge commit
            if (commit_message.startswith('merge pull request') or 
                commit_message.startswith('merge branch') or
                'merge' in commit_message and 'pull request' in commit_message):
                print(f"Skipping push event - appears to be a merge commit: {commit_message}")
                return None

        ist = pytz.timezone('Asia/Kolkata')
        timestamp = datetime.now(pytz.utc).astimezone(ist)
        
        return {
            'action': 'PUSH',
            'author': author,
            'to_branch': to_branch,
            'from_branch': None,
            'timestamp': timestamp,
            'formatted_message': f'"{author}" pushed to "{to_branch}" on {timestamp.strftime("%d %B %Y - %I:%M %p UTC")}'
        }
    except KeyError as e:
        print(f"Error processing push event: {e}")
        return None

def process_pull_request_event(payload):
    try:
        # Only process when PR is opened
        if payload['action'] != 'opened':
            return None
            
        author = payload['pull_request']['user']['login']
        from_branch = payload['pull_request']['head']['ref']
        to_branch = payload['pull_request']['base']['ref']

        ist = pytz.timezone('Asia/Kolkata')
        timestamp = datetime.now(pytz.utc).astimezone(ist)
        
        return {
            'action': 'PULL_REQUEST',
            'author': author,
            'from_branch': from_branch,
            'to_branch': to_branch,
            'timestamp': timestamp,
            'formatted_message': f'"{author}" submitted a pull request from "{from_branch}" to "{to_branch}" on {timestamp.strftime("%d %B %Y - %I:%M %p UTC")}'
        }
    except KeyError as e:
        print(f"Error processing pull request event: {e}")
        return None

def process_merge_event(payload):
    try:
        # This handles pull_request events with action 'closed' and merged = true
        author = payload['pull_request']['merged_by']['login']
        from_branch = payload['pull_request']['head']['ref']
        to_branch = payload['pull_request']['base']['ref']

        ist = pytz.timezone('Asia/Kolkata')
        timestamp = datetime.now(pytz.utc).astimezone(ist)
        
        return {
            'action': 'MERGE',
            'author': author,
            'from_branch': from_branch,
            'to_branch': to_branch,
            'timestamp': timestamp,
            'formatted_message': f'"{author}" merged branch "{from_branch}" to "{to_branch}" on {timestamp.strftime("%d %B %Y - %I:%M %p UTC")}'
        }
    except KeyError as e:
        print(f"Error processing merge event: {e}")
        return None


@ui_bp.route('/')
def index():
    """Render the main dashboard page"""
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"Error rendering template: {e}")
        return f"""
        <html>
        <head><title>GitHub Webhook Events</title></head>
        <body>
            <h1>GitHub Webhook Events Dashboard</h1>
            <p>Error loading template: {str(e)}</p>
            <p>Please check if templates/index.html exists in the app directory.</p>
            <p><a href="/api/events">View Raw Events JSON</a></p>
        </body>
        </html>
        """, 500



@ui_bp.route('/api/events')
def get_events():
    try:
        events = mongo.get_latest_events()
        # Convert ObjectId to string for JSON serialization
        for event in events:
            if '_id' in event:
                event['_id'] = str(event['_id'])
            # Convert datetime to string
            if 'timestamp' in event:
                event['timestamp'] = event['timestamp'].isoformat()
        
        return jsonify({
            'events': events,
            'total_count': mongo.get_event_count(),
            'status': 'success'
        })
    except Exception as e:
        print(f"Error in get_events: {e}")
        return jsonify({'error': str(e), 'status': 'error'}), 500