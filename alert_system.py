"""
Alert System for AquaVision AI
Handles email notifications and desktop alerts for disease detections
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from typing import Optional, List
import os
from datetime import datetime

try:
    from plyer import notification
    DESKTOP_NOTIFICATIONS_AVAILABLE = True
except ImportError:
    DESKTOP_NOTIFICATIONS_AVAILABLE = False
    print("⚠️ Desktop notifications not available. Install plyer: pip install plyer")


class AlertSystem:
    """Manages email and desktop notifications for disease detections"""
    
    def __init__(self, email_enabled: bool = False, desktop_enabled: bool = True):
        """
        Initialize alert system
        
        Args:
            email_enabled: Enable email notifications
            desktop_enabled: Enable desktop notifications
        """
        self.email_enabled = email_enabled
        self.desktop_enabled = desktop_enabled and DESKTOP_NOTIFICATIONS_AVAILABLE
        
        # Email configuration (user should set these)
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = None
        self.sender_password = None
        self.recipient_emails = []
        
        # Alert thresholds
        self.disease_alert_threshold = 0.7  # Alert if disease confidence > 70%
        self.critical_diseases = [
            "White Tail Disease",
            "Viral Disease",
            "Parasitic Disease"
        ]
    
    def configure_email(self, sender_email: str, sender_password: str, 
                       recipients: List[str], smtp_server: str = "smtp.gmail.com",
                       smtp_port: int = 587):
        """
        Configure email settings
        
        Args:
            sender_email: Gmail address to send from
            sender_password: App password (not regular password)
            recipients: List of recipient email addresses
            smtp_server: SMTP server address
            smtp_port: SMTP port
        """
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.recipient_emails = recipients
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email_enabled = True
    
    def should_alert(self, disease: str, confidence: float) -> bool:
        """
        Determine if alert should be sent
        
        Args:
            disease: Detected disease name
            confidence: Detection confidence (0-1)
        
        Returns:
            True if alert should be sent
        """
        # Alert for critical diseases even with lower confidence
        if any(critical in disease for critical in self.critical_diseases):
            return confidence > 0.5
        
        # Alert for other diseases only if confidence is high
        if "Healthy" in disease:
            return False
        
        return confidence > self.disease_alert_threshold
    
    def send_desktop_alert(self, title: str, message: str, timeout: int = 10):
        """
        Send desktop notification
        
        Args:
            title: Notification title
            message: Notification message
            timeout: Notification timeout in seconds
        """
        if not self.desktop_enabled:
            return False
        
        try:
            notification.notify(
                title=title,
                message=message,
                app_name="AquaVision AI",
                timeout=timeout,
                app_icon=None  # Can add custom icon path
            )
            return True
        except Exception as e:
            print(f"Desktop notification error: {e}")
            return False
    
    def send_email_alert(self, subject: str, body: str, 
                        attachments: List[str] = []) -> bool:
        """
        Send email alert
        
        Args:
            subject: Email subject
            body: Email body (HTML supported)
            image_path: Optional path to attach image
        
        Returns:
            True if email sent successfully
        """
        if not self.email_enabled or not self.sender_email:
            print("Email not configured")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = ', '.join(self.recipient_emails)
            msg['Subject'] = subject
            
            # Add body
            html_body = f"""
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                padding: 20px; color: white; border-radius: 10px 10px 0 0;">
                        <h2>🐟 AquaVision AI Alert</h2>
                    </div>
                    <div style="padding: 20px; background: #f5f5f5; border-radius: 0 0 10px 10px;">
                        {body}
                        <hr style="margin: 20px 0; border: none; border-top: 1px solid #ddd;">
                        <p style="color: #666; font-size: 12px;">
                            This is an automated alert from AquaVision AI<br>
                            Sent at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                        </p>
                    </div>
                </body>
            </html>
            """
            msg.attach(MIMEText(html_body, 'html'))
            
            # Attach images if provided
            if attachments:
                for file_path in attachments:
                    if file_path and os.path.exists(file_path):
                        try:
                            with open(file_path, 'rb') as f:
                                img_data = f.read()
                                img = MIMEImage(img_data)
                                img.add_header('Content-Disposition', 'attachment', 
                                             filename=os.path.basename(file_path))
                                msg.attach(img)
                        except Exception as e:
                            print(f"Failed to attach {file_path}: {e}")
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            print(f"[OK] Email alert sent to {len(self.recipient_emails)} recipients")
            return True
            
        except Exception as e:
            print(f"[ERROR] Email sending failed: {e}")
            return False
    
    def send_disease_detection_alert(self, species: str, disease: str, 
                                    confidence: float, image_path: Optional[str] = None,
                                    notes: Optional[str] = None):
        """
        Send alert for disease detection
        
        Args:
            species: Detected species
            disease: Detected disease
            confidence: Detection confidence
            image_path: Path to analyzed image
            notes: Additional notes
        """
        if not self.should_alert(disease, confidence):
            return
        
        # Determine severity
        is_critical = any(critical in disease for critical in self.critical_diseases)
        severity = "CRITICAL" if is_critical else "WARNING"
        
        # Desktop notification
        desktop_title = f"🚨 {severity}: {disease} Detected"
        desktop_message = f"Species: {species}\nConfidence: {confidence*100:.1f}%"
        self.send_desktop_alert(desktop_title, desktop_message)
        
        # Email notification
        email_subject = f"[{severity}] AquaVision AI - {disease} Detected"
        
        severity_color = "#dc3545" if is_critical else "#ffc107"
        email_body = f"""
        <div style="background: {severity_color}; color: white; padding: 15px; 
                    border-radius: 5px; margin-bottom: 20px;">
            <h3 style="margin: 0;">⚠️ {severity} ALERT</h3>
        </div>
        
        <h3>Disease Detection Summary</h3>
        <table style="width: 100%; border-collapse: collapse;">
            <tr style="background: #f0f0f0;">
                <td style="padding: 10px; border: 1px solid #ddd;"><strong>Species:</strong></td>
                <td style="padding: 10px; border: 1px solid #ddd;">{species}</td>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;"><strong>Disease:</strong></td>
                <td style="padding: 10px; border: 1px solid #ddd; color: #dc3545;">
                    <strong>{disease}</strong>
                </td>
            </tr>
            <tr style="background: #f0f0f0;">
                <td style="padding: 10px; border: 1px solid #ddd;"><strong>Confidence:</strong></td>
                <td style="padding: 10px; border: 1px solid #ddd;">{confidence*100:.1f}%</td>
            </tr>
        </table>
        
        <h3 style="margin-top: 20px;">Recommended Action</h3>
        <div style="background: #e3f2fd; padding: 15px; border-left: 4px solid #2196f3; 
                    margin: 10px 0;">
            <ul style="margin: 0; padding-left: 20px;">
                {"<li>🚨 <strong>Immediate attention required</strong> - Isolate affected fish</li>" if is_critical else ""}
                <li>📋 Consult treatment recommendations in AquaVision AI</li>
                <li>💊 Begin appropriate treatment protocol</li>
                <li>🔬 Monitor fish closely for next 24-48 hours</li>
                <li>💧 Check and maintain water quality parameters</li>
            </ul>
        </div>
        
        {f'<h3>Additional Notes</h3><p style="background: #fff3cd; padding: 10px; border-radius: 5px;">{notes}</p>' if notes else ''}
        
        <div style="background: #d4edda; padding: 15px; border-radius: 5px; margin-top: 20px;">
            <strong>💡 Tip:</strong> Open AquaVision AI to view detailed treatment information 
            and track this detection in your history.
        </div>
        """
        
        self.send_email_alert(email_subject, email_body, image_path)
    
    def send_batch_summary_alert(self, detections: List[dict]):
        """
        Send summary of batch detections
        
        Args:
            detections: List of detection dictionaries
        """
        if not detections:
            return
        
        diseased_count = sum(1 for d in detections if "Healthy" not in d.get('disease', ''))
        
        desktop_message = f"Analyzed {len(detections)} fish\n{diseased_count} disease(s) detected"
        self.send_desktop_alert("📊 Batch Analysis Complete", desktop_message)
        
        # Create summary table
        summary_rows = ""
        for i, d in enumerate(detections[:10], 1):  # Show first 10
            disease_color = "#dc3545" if "Healthy" not in d.get('disease', '') else "#28a745"
            summary_rows += f"""
            <tr style="{"background: #fff3cd;" if "Healthy" not in d.get('disease', '') else ""}">
                <td style="padding: 8px; border: 1px solid #ddd;">{i}</td>
                <td style="padding: 8px; border: 1px solid #ddd;">{d.get('species', 'Unknown')}</td>
                <td style="padding: 8px; border: 1px solid #ddd; color: {disease_color};">
                    {d.get('disease', 'Unknown')}
                </td>
                <td style="padding: 8px; border: 1px solid #ddd;">{d.get('confidence', 0)*100:.1f}%</td>
            </tr>
            """
        
        email_body = f"""
        <h3>Batch Analysis Summary</h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 20px 0;">
            <div style="background: #e3f2fd; padding: 15px; border-radius: 5px; text-align: center;">
                <h2 style="margin: 0; color: #1976d2;">{len(detections)}</h2>
                <p style="margin: 5px 0 0 0;">Total Fish Analyzed</p>
            </div>
            <div style="background: #ffebee; padding: 15px; border-radius: 5px; text-align: center;">
                <h2 style="margin: 0; color: #d32f2f;">{diseased_count}</h2>
                <p style="margin: 5px 0 0 0;">Diseases Detected</p>
            </div>
        </div>
        
        <h3>Detection Details</h3>
        <table style="width: 100%; border-collapse: collapse;">
            <thead>
                <tr style="background: #f0f0f0;">
                    <th style="padding: 10px; border: 1px solid #ddd;">#</th>
                    <th style="padding: 10px; border: 1px solid #ddd;">Species</th>
                    <th style="padding: 10px; border: 1px solid #ddd;">Health Status</th>
                    <th style="padding: 10px; border: 1px solid #ddd;">Confidence</th>
                </tr>
            </thead>
            <tbody>
                {summary_rows}
            </tbody>
        </table>
        
        {f'<p style="margin-top: 10px; color: #666;">Showing first 10 of {len(detections)} detections</p>' if len(detections) > 10 else ''}
        """
        
        self.send_email_alert(
            f"📊 Batch Analysis Complete - {diseased_count} Disease(s) Found",
            email_body
        )
    
    def send_water_quality_alert(self, parameter: str, value: float, 
                                 safe_range: tuple):
        """
        Send alert for unsafe water quality
        
        Args:
            parameter: Parameter name (pH, ammonia, etc.)
            value: Measured value
            safe_range: Tuple of (min, max) safe values
        """
        desktop_message = f"{parameter}: {value}\nSafe range: {safe_range[0]}-{safe_range[1]}"
        self.send_desktop_alert(
            f"⚠️ Water Quality Alert: {parameter}",
            desktop_message
        )
        
        email_body = f"""
        <div style="background: #ff6b6b; color: white; padding: 15px; 
                    border-radius: 5px; margin-bottom: 20px;">
            <h3 style="margin: 0;">💧 Water Quality Alert</h3>
        </div>
        
        <h3>Parameter Out of Range</h3>
        <table style="width: 100%; border-collapse: collapse;">
            <tr style="background: #f0f0f0;">
                <td style="padding: 10px; border: 1px solid #ddd;"><strong>Parameter:</strong></td>
                <td style="padding: 10px; border: 1px solid #ddd;">{parameter}</td>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;"><strong>Current Value:</strong></td>
                <td style="padding: 10px; border: 1px solid #ddd; color: #dc3545;">
                    <strong>{value}</strong>
                </td>
            </tr>
            <tr style="background: #f0f0f0;">
                <td style="padding: 10px; border: 1px solid #ddd;"><strong>Safe Range:</strong></td>
                <td style="padding: 10px; border: 1px solid #ddd;">{safe_range[0]} - {safe_range[1]}</td>
            </tr>
        </table>
        
        <h3 style="margin-top: 20px;">Recommended Actions</h3>
        <div style="background: #e3f2fd; padding: 15px; border-left: 4px solid #2196f3;">
            <ul style="margin: 0; padding-left: 20px;">
                <li>Perform immediate water testing to confirm values</li>
                <li>Conduct partial water change (20-30%)</li>
                <li>Check filtration system operation</li>
                <li>Monitor fish behavior closely</li>
                <li>Retest water parameters in 24 hours</li>
            </ul>
        </div>
        """
        
        self.send_email_alert(
            f"⚠️ Water Quality Alert - {parameter} Out of Range",
            email_body
        )
    
    def test_notifications(self):
        """Test both notification systems"""
        print("\n🧪 Testing Alert System...\n")
        
        # Test desktop notification
        if self.desktop_enabled:
            print("Testing desktop notification...")
            success = self.send_desktop_alert(
                "🧪 AquaVision AI Test",
                "Desktop notifications are working!"
            )
            print(f"  {'✅' if success else '❌'} Desktop notification")
        else:
            print("  ⚠️ Desktop notifications not available")
        
        # Test email notification
        if self.email_enabled:
            print("\nTesting email notification...")
            success = self.send_email_alert(
                "🧪 AquaVision AI Test Email",
                "<h3>Test Successful!</h3><p>Email notifications are working correctly.</p>"
            )
            print(f"  {'✅' if success else '❌'} Email notification")
        else:
            print("  ⚠️ Email not configured")
        
        print("\n✅ Alert system test complete!\n")


# Singleton instance
_alert_instance = None

def get_alert_system() -> AlertSystem:
    """Get singleton alert system instance"""
    global _alert_instance
    if _alert_instance is None:
        _alert_instance = AlertSystem()
    return _alert_instance


if __name__ == "__main__":
    # Demo usage
    alert = AlertSystem()
    alert.test_notifications()
