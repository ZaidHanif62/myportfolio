from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from .models import Profile, Skill, Project, Experience, Education, ContactMessage

def home(request):
    profile = Profile.objects.first()
    skills = Skill.objects.all()
    projects = Project.objects.filter(featured=True)[:6]
    experiences = Experience.objects.all()[:3]
    
    context = {
        'profile': profile,
        'skills': skills,
        'projects': projects,
        'experiences': experiences,
    }
    return render(request, 'portfolio/home.html', context)

def about(request):
    profile = Profile.objects.first()
    skills = Skill.objects.all()
    experiences = Experience.objects.all()
    educations = Education.objects.all()
    
    context = {
        'profile': profile,
        'skills': skills,
        'experiences': experiences,
        'educations': educations,
    }
    return render(request, 'portfolio/about.html', context)

def projects(request):
    all_projects = Project.objects.all()
    profile = Profile.objects.first()
    
    context = {
        'projects': all_projects,
        'profile': profile,
    }
    return render(request, 'portfolio/projects.html', context)

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    profile = Profile.objects.first()
    related_projects = Project.objects.exclude(slug=slug)[:3]
    
    context = {
        'project': project,
        'profile': profile,
        'related_projects': related_projects,
    }
    return render(request, 'portfolio/project_detail.html', context)

def contact(request):
    profile = Profile.objects.first()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Save to database
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        # Send email notification
        try:
            # Email to you (site owner) - HTML Version
            email_subject = f'New Portfolio Contact: {subject}'
            
            # Plain text version
            text_content = f'''
New Contact Form Submission from Portfolio

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}

---
Sent from your portfolio website contact form.
Reply directly to this email to respond to {name}.
            '''
            
            # HTML version
            html_content = f'''
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                    <h1 style="color: white; margin: 0;">New Contact Message</h1>
                </div>
                
                <div style="padding: 30px; background: #f8f9fa; border-radius: 0 0 10px 10px;">
                    <div style="background: white; padding: 25px; border-radius: 8px; margin-bottom: 20px;">
                        <h2 style="color: #667eea; margin-top: 0;">Contact Details</h2>
                        <p style="margin: 10px 0;"><strong>Name:</strong> {name}</p>
                        <p style="margin: 10px 0;"><strong>Email:</strong> <a href="mailto:{email}" style="color: #667eea;">{email}</a></p>
                        <p style="margin: 10px 0;"><strong>Subject:</strong> {subject}</p>
                    </div>
                    
                    <div style="background: white; padding: 25px; border-radius: 8px;">
                        <h3 style="color: #667eea; margin-top: 0;">Message:</h3>
                        <p style="background: #f8f9fa; padding: 15px; border-left: 4px solid #667eea; border-radius: 4px; line-height: 1.8;">
                            {message}
                        </p>
                    </div>
                    
                    <div style="margin-top: 20px; padding: 15px; background: #e3f2fd; border-radius: 8px; text-align: center;">
                        <p style="margin: 0; color: #1976d2;">
                            <strong>Quick Action:</strong> Reply directly to this email to respond to {name}
                        </p>
                    </div>
                    
                    <p style="text-align: center; color: #888; font-size: 12px; margin-top: 20px;">
                        Sent from your portfolio website contact form
                    </p>
                </div>
            </body>
            </html>
            '''
            
            # Create email with both text and HTML
            owner_email = EmailMultiAlternatives(
                email_subject,
                text_content,
                settings.DEFAULT_FROM_EMAIL,
                ['zaidhanif62@gmail.com'],
                reply_to=[email],  # This allows you to reply directly
            )
            owner_email.attach_alternative(html_content, "text/html")
            owner_email.send()
            
            # Auto-reply to sender - HTML Version
            auto_reply_subject = f'Thank you for contacting me - {subject}'
            
            # Plain text auto-reply
            auto_reply_text = f'''
Hello {name},

Thank you for reaching out through my portfolio website! I have received your message and will get back to you as soon as possible.

Your message:
"{message}"

I typically respond within 24-48 hours. If your inquiry is urgent, feel free to send a follow-up email.

Best regards,
{profile.name if profile else "Zaid Hanif"}

---
This is an automated response from zaidhanif62@gmail.com
            '''
            
            # HTML auto-reply
            auto_reply_html = f'''
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                    <h1 style="color: white; margin: 0;">Thank You for Reaching Out!</h1>
                </div>
                
                <div style="padding: 30px; background: #f8f9fa; border-radius: 0 0 10px 10px;">
                    <div style="background: white; padding: 25px; border-radius: 8px; margin-bottom: 20px;">
                        <p style="font-size: 16px; margin-top: 0;">Hello <strong>{name}</strong>,</p>
                        
                        <p>Thank you for contacting me through my portfolio website! I have received your message and will respond as soon as possible.</p>
                        
                        <div style="background: #f8f9fa; padding: 15px; border-left: 4px solid #667eea; border-radius: 4px; margin: 20px 0;">
                            <p style="margin: 0; color: #666;"><strong>Your message:</strong></p>
                            <p style="margin: 10px 0 0 0; line-height: 1.8;">"{message}"</p>
                        </div>
                        
                        <p>I typically respond within <strong>24-48 hours</strong>. If your inquiry is urgent, feel free to send a follow-up email.</p>
                        
                        <p style="margin-top: 30px;">Best regards,<br>
                        <strong>{profile.name if profile else "Zaid Hanif"}</strong></p>
                    </div>
                    
                    <div style="text-align: center; padding: 20px;">
                        <p style="color: #888; font-size: 12px; margin: 0;">
                            This is an automated response. Please do not reply to this email.<br>
                            For urgent matters, contact: zaidhanif62@gmail.com
                        </p>
                    </div>
                </div>
            </body>
            </html>
            '''
            
            # Send auto-reply
            auto_reply_email = EmailMultiAlternatives(
                auto_reply_subject,
                auto_reply_text,
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
            auto_reply_email.attach_alternative(auto_reply_html, "text/html")
            auto_reply_email.send(fail_silently=True)
            
            messages.success(request, '✅ Thank you! Your message has been sent successfully. I will get back to you soon.')
            
        except Exception as e:
            messages.warning(request, f'⚠️ Your message was saved but email notification failed. Please try again or contact directly at zaidhanif62@gmail.com')
            print(f"Email Error: {str(e)}")  # For debugging
        
        return redirect('contact')
    
    context = {
        'profile': profile,
    }
    return render(request, 'portfolio/contact.html', context)