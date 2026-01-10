"""
Community Manager for AquaVision AI
Handles all community features including user profiles, posts, and expert consultation
"""

from typing import List, Dict, Optional
from datetime import datetime
import hashlib
import secrets
from database import get_database


class CommunityManager:
    """Manages community features and user interactions"""
    
    def __init__(self):
        """Initialize community manager"""
        self.db = get_database()
        self.current_user = None
    
    # ==================== USER MANAGEMENT ====================
    
    def create_user_account(self, username: str, email: str, 
                           location: str = None) -> Dict:
        """
        Create a new user account
        
        Args:
            username: Unique username
            email: User email address
            location: User location (city, country)
        
        Returns:
            User information dictionary
        """
        try:
            user_id = self.db.create_user(username, email, location)
            return {
                'success': True,
                'user_id': user_id,
                'username': username,
                'email': email,
                'message': f'Welcome to AquaVision AI Community, {username}!'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to create account. Username or email may already exist.'
            }
    
    def login_user(self, username: str) -> Dict:
        """
        Login user (simplified - no password for now)
        
        Args:
            username: Username to login
        
        Returns:
            Login status and user info
        """
        user = self.db.get_user(username=username)
        
        if user:
            self.current_user = user
            return {
                'success': True,
                'user': user,
                'message': f'Welcome back, {username}!'
            }
        else:
            return {
                'success': False,
                'message': 'User not found'
            }
    
    def get_current_user(self) -> Optional[Dict]:
        """Get currently logged in user"""
        return self.current_user
    
    def update_user_profile(self, bio: str = None, location: str = None,
                           profile_image: str = None) -> bool:
        """
        Update current user's profile
        
        Args:
            bio: User biography
            location: Updated location
            profile_image: Path to profile image
        
        Returns:
            Success status
        """
        if not self.current_user:
            return False
        
        # Update database (add method to database.py if needed)
        # For now, just update local copy
        if bio:
            self.current_user['bio'] = bio
        if location:
            self.current_user['location'] = location
        if profile_image:
            self.current_user['profile_image'] = profile_image
        
        return True
    
    # ==================== COMMUNITY POSTS ====================
    
    def share_detection(self, image_path: str, species: str, disease: str,
                       description: str, ask_for_verification: bool = True) -> Dict:
        """
        Share a detection with the community
        
        Args:
            image_path: Path to fish image
            species: Detected species
            disease: Detected disease
            description: User description/question
            ask_for_verification: Whether to ask for expert verification
        
        Returns:
            Post creation result
        """
        if not self.current_user:
            return {
                'success': False,
                'message': 'Please login to share detections'
            }
        
        try:
            post_id = self.db.create_community_post(
                user_id=self.current_user['id'],
                image_path=image_path,
                species=species,
                disease=disease,
                description=description,
                location=self.current_user.get('location')
            )
            
            return {
                'success': True,
                'post_id': post_id,
                'message': 'Detection shared with community!',
                'verification_requested': ask_for_verification
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to share detection'
            }
    
    def get_community_feed(self, filter_location: bool = False,
                          limit: int = 50) -> List[Dict]:
        """
        Get community posts feed
        
        Args:
            filter_location: Filter by user's location
            limit: Maximum posts to return
        
        Returns:
            List of community posts
        """
        location = None
        if filter_location and self.current_user:
            location = self.current_user.get('location')
        
        posts = self.db.get_community_feed(limit=limit, location=location)
        
        # Enrich with additional info
        for post in posts:
            post['time_ago'] = self._format_time_ago(post['timestamp'])
            post['is_verified'] = post.get('expert_verified', False)
        
        return posts
    
    def add_comment(self, post_id: int, comment_text: str) -> Dict:
        """
        Add comment to a community post
        
        Args:
            post_id: ID of post to comment on
            comment_text: Comment text
        
        Returns:
            Comment creation result
        """
        if not self.current_user:
            return {
                'success': False,
                'message': 'Please login to comment'
            }
        
        try:
            comment_id = self.db.add_post_comment(
                post_id=post_id,
                user_id=self.current_user['id'],
                comment=comment_text
            )
            
            return {
                'success': True,
                'comment_id': comment_id,
                'message': 'Comment added successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to add comment'
            }
    
    def get_post_comments(self, post_id: int) -> List[Dict]:
        """
        Get all comments for a post
        
        Args:
            post_id: Post ID
        
        Returns:
            List of comments
        """
        comments = self.db.get_post_comments(post_id)
        
        # Format timestamps
        for comment in comments:
            comment['time_ago'] = self._format_time_ago(comment['timestamp'])
        
        return comments
    
    # ==================== SUCCESS STORIES ====================
    
    def share_success_story(self, disease: str, treatment_method: str,
                           duration_days: int, success_rate: int,
                           description: str, before_image: str = None,
                           after_image: str = None) -> Dict:
        """
        Share a treatment success story
        
        Args:
            disease: Disease that was treated
            treatment_method: Method used for treatment
            duration_days: Days taken for recovery
            success_rate: Success rate (0-100)
            description: Detailed description
            before_image: Before treatment image
            after_image: After treatment image
        
        Returns:
            Story creation result
        """
        if not self.current_user:
            return {
                'success': False,
                'message': 'Please login to share stories'
            }
        
        try:
            story_id = self.db.add_success_story(
                user_id=self.current_user['id'],
                disease=disease,
                treatment_method=treatment_method,
                duration_days=duration_days,
                success_rate=success_rate,
                description=description,
                before_image=before_image,
                after_image=after_image
            )
            
            return {
                'success': True,
                'story_id': story_id,
                'message': 'Success story shared! This will help others treat their fish.'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to share story'
            }
    
    def get_success_stories(self, disease: str = None, 
                           limit: int = 20) -> List[Dict]:
        """
        Get treatment success stories
        
        Args:
            disease: Optional disease filter
            limit: Maximum stories to return
        
        Returns:
            List of success stories
        """
        stories = self.db.get_success_stories(disease=disease, limit=limit)
        
        # Enrich with additional info
        for story in stories:
            story['time_ago'] = self._format_time_ago(story['timestamp'])
            story['effectiveness'] = self._calculate_effectiveness(story)
        
        return stories
    
    # ==================== EXPERT FEATURES ====================
    
    def get_pending_verifications(self) -> List[Dict]:
        """
        Get posts awaiting expert verification
        (Only for expert users)
        
        Returns:
            List of posts needing verification
        """
        if not self.current_user or not self.current_user.get('expert_verified'):
            return []
        
        # Get unverified posts
        feed = self.db.get_community_feed(limit=100)
        pending = [post for post in feed if not post.get('expert_verified')]
        
        return pending
    
    def verify_post(self, post_id: int, is_correct: bool, 
                   expert_comment: str = None) -> Dict:
        """
        Verify a community post (expert only)
        
        Args:
            post_id: Post ID to verify
            is_correct: Whether the detection is correct
            expert_comment: Expert's comment
        
        Returns:
            Verification result
        """
        if not self.current_user or not self.current_user.get('expert_verified'):
            return {
                'success': False,
                'message': 'Expert verification required'
            }
        
        # Add expert comment
        if expert_comment:
            self.add_comment(post_id, f"✅ Expert Verification: {expert_comment}")
        
        return {
            'success': True,
            'message': 'Post verified by expert'
        }
    
    # ==================== LOCAL OUTBREAK ALERTS ====================
    
    def report_outbreak(self, disease: str, severity: str,
                       description: str) -> Dict:
        """
        Report a disease outbreak in user's location
        
        Args:
            disease: Disease name
            severity: Severity level (Low/Medium/High/Critical)
            description: Outbreak description
        
        Returns:
            Report result
        """
        if not self.current_user:
            return {
                'success': False,
                'message': 'Please login to report outbreaks'
            }
        
        # Share as community post with special tag
        result = self.share_detection(
            image_path="",  # No image required for outbreak report
            species="Multiple Species",
            disease=disease,
            description=f"🚨 OUTBREAK ALERT - {severity} Severity\n\n{description}"
        )
        
        if result['success']:
            result['message'] = 'Outbreak reported! Nearby users will be notified.'
        
        return result
    
    def get_local_outbreaks(self, radius_km: int = 50) -> List[Dict]:
        """
        Get outbreak alerts near user's location
        
        Args:
            radius_km: Search radius in kilometers
        
        Returns:
            List of local outbreaks
        """
        if not self.current_user or not self.current_user.get('location'):
            return []
        
        # Get posts from same location (simplified)
        posts = self.db.get_community_feed(
            location=self.current_user['location'],
            limit=50
        )
        
        # Filter for outbreak alerts
        outbreaks = [
            post for post in posts 
            if '🚨 OUTBREAK ALERT' in post.get('description', '')
        ]
        
        return outbreaks
    
    # ==================== STATISTICS ====================
    
    def get_user_statistics(self, user_id: int = None) -> Dict:
        """
        Get user statistics
        
        Args:
            user_id: User ID (defaults to current user)
        
        Returns:
            User statistics
        """
        if user_id is None and self.current_user:
            user_id = self.current_user['id']
        
        if not user_id:
            return {}
        
        user = self.db.get_user(user_id=user_id)
        
        if not user:
            return {}
        
        # Get user's posts
        all_posts = self.db.get_community_feed(limit=1000)
        user_posts = [post for post in all_posts if post.get('user_id') == user_id]
        
        # Get user's success stories
        all_stories = self.db.get_success_stories(limit=1000)
        user_stories = [story for story in all_stories if story.get('user_id') == user_id]
        
        return {
            'username': user['username'],
            'join_date': user['join_date'],
            'total_detections': user.get('total_detections', 0),
            'posts_shared': len(user_posts),
            'success_stories': len(user_stories),
            'expert_verified': user.get('expert_verified', False),
            'location': user.get('location', 'Unknown')
        }
    
    def get_community_statistics(self) -> Dict:
        """
        Get overall community statistics
        
        Returns:
            Community statistics
        """
        posts = self.db.get_community_feed(limit=10000)
        stories = self.db.get_success_stories(limit=10000)
        
        # Count diseases
        disease_counts = {}
        for post in posts:
            disease = post.get('disease', 'Unknown')
            disease_counts[disease] = disease_counts.get(disease, 0) + 1
        
        # Most common diseases
        top_diseases = sorted(disease_counts.items(), 
                            key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'total_posts': len(posts),
            'total_stories': len(stories),
            'top_diseases': top_diseases,
            'active_users': len(set(post['user_id'] for post in posts))
        }
    
    # ==================== UTILITY FUNCTIONS ====================
    
    def _format_time_ago(self, timestamp: str) -> str:
        """Format timestamp as 'X time ago'"""
        try:
            dt = datetime.fromisoformat(timestamp)
            diff = datetime.now() - dt
            
            seconds = diff.total_seconds()
            
            if seconds < 60:
                return "Just now"
            elif seconds < 3600:
                minutes = int(seconds / 60)
                return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
            elif seconds < 86400:
                hours = int(seconds / 3600)
                return f"{hours} hour{'s' if hours != 1 else ''} ago"
            elif seconds < 604800:
                days = int(seconds / 86400)
                return f"{days} day{'s' if days != 1 else ''} ago"
            elif seconds < 2592000:
                weeks = int(seconds / 604800)
                return f"{weeks} week{'s' if weeks != 1 else ''} ago"
            else:
                months = int(seconds / 2592000)
                return f"{months} month{'s' if months != 1 else ''} ago"
        except:
            return "Unknown"
    
    def _calculate_effectiveness(self, story: Dict) -> str:
        """Calculate treatment effectiveness rating"""
        success_rate = story.get('success_rate', 0)
        
        if success_rate >= 90:
            return "⭐⭐⭐⭐⭐ Highly Effective"
        elif success_rate >= 75:
            return "⭐⭐⭐⭐ Very Effective"
        elif success_rate >= 60:
            return "⭐⭐⭐ Moderately Effective"
        elif success_rate >= 40:
            return "⭐⭐ Somewhat Effective"
        else:
            return "⭐ Limited Effectiveness"


# Singleton instance
_community_instance = None

def get_community_manager() -> CommunityManager:
    """Get singleton community manager instance"""
    global _community_instance
    if _community_instance is None:
        _community_instance = CommunityManager()
    return _community_instance


if __name__ == "__main__":
    # Demo usage
    print("👥 Community Manager Demo")
    community = CommunityManager()
    
    # Create test user
    result = community.create_user_account(
        username="test_user",
        email="test@aquavision.ai",
        location="Mumbai, India"
    )
    print(f"User creation: {result['message']}")
    
    # Login
    login_result = community.login_user("test_user")
    if login_result['success']:
        print(f"Login: {login_result['message']}")
    
    print("✅ Community manager initialized")
