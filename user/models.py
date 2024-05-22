from django.db import models
from multiselectfield import MultiSelectField
from ckeditor.fields import RichTextField

from django.contrib.auth.models import User


class Skill(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
class Interest(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Profile(models.Model):
    SKILLS = (
        ('HTML', 'HTML'),
        ('CSS', 'CSS'),
        ('JavaScript', 'JavaScript'),
        ('TypeScript', 'TypeScript'),
        ('NodeJS', 'NodeJS'),
        ('Express', 'Express'),
        ('Next', 'Next'),
        ('Nust', 'Nust'),
        ('React', 'React'),
        ('Angular', 'Angular'),
        ('Vue', 'Vue'),
        ('GIT', 'GIT'),
        ('Python', 'Python'),
        ('Ruby', 'Ruby'),
        ('Django', 'Django'),
        ('Flask', 'Flask'),
        ('FastAPI', 'FastAPI'),
        ('Java', 'Java'),
        ('Spring', 'Spring'),
        ('Docker', 'Docker'),
        ('React Native', 'React Native'),
        ('Swift', 'Swift'),
        ('Kotlin', 'Kotlin'),
        ('PHP', 'PHP'),
        ('Laravel', 'Laravel'),
        ('C', 'C'),
        ('C++', 'C++'),
        ('C#', 'C#'),
        ('Blender', 'Blender'),
        ('Unity', 'Unity'),
        ('Unity', 'Unity'),
        ('Unreal Engine', 'Unreal Engine'),
        ('Maya', 'Maya'),
        ('Cinema 4D', 'Cinema 4D'),
        ('3D Modeling', '3D Modeling'),
        ('Blockchain Technology', 'Blockchain Technology'),
        ('Smart Contracts', 'Smart Contracts'),
        ('Solidity', 'Solidity'),
        ('Ethereum', 'Ethereum'),
        ('Hyperledger', 'Hyperledger'),
        ('Bitcoin', 'Bitcoin'),
        ('Cryptocurrency', 'Cryptocurrency'),
        ('Decentralized Applications (DApps)', 'Decentralized Applications (DApps)'),
        ('UI/UX Design', 'UI/UX Design'),
        ('Adobe Photoshop', 'Adobe Photoshop'),
        ('Adobe Illustrator', 'Adobe Illustrator'),
        ('Sketch', 'Sketch'),
        ('Figma', 'Figma'),
        ('Prototyping', 'Prototyping'),
        ('Responsive Design', 'Responsive Design'),
        ('Typography', 'Typography'),
        ('Cybersecurity', 'Cybersecurity'),
        ('Ethical Hacking', 'Ethical Hacking'),
        ('Network Security', 'Network Security'),
        ('Vulnerability Assessment', 'Vulnerability Assessment'),
        ('Penetration Testing', 'Penetration Testing'),
        ('Security Auditing', 'Security Auditing'),
        ('Incident Response', 'Incident Response'),
        ('Security Tools (e.g., Nmap, Wireshark)', 'Security Tools (e.g., Nmap, Wireshark)'),
        ('Continuous Integration (CI)', 'Continuous Integration (CI)'),
        ('Continuous Deployment (CD)', 'Continuous Deployment (CD)'),
        ('Kubernetes', 'Kubernetes'),
        ('Infrastructure as Code (IaC)', 'Infrastructure as Code (IaC)'),
        ('Configuration Management', 'Configuration Management'),
        ('Monitoring and Logging', 'Monitoring and Logging'),
    )
    
    INTERESTS = (
        ('3d modeling', '3d modeling'),
        ('Communication', 'Communication'),
        ('Design', 'Design'),
        ('Education', 'Education'),
        ('Gaming', 'Gaming'),
        ('Lifehacks', 'Lifehacks'),
        ('Mobile', 'Mobile'),
        ('Productivity', 'Productivity'),
        ('Cybersecurity', 'Cybersecurity'),
        ('DevOps', 'DevOps'),
        ('Enterprise', 'Enterprise'),
        ('Health', 'Health'),
        ('Low/No Code', 'Low/No Code'),
        ('Music/Art', 'Music/Art'),
        ('Voice skills', 'Voice skills'),
        ('Blockchain', 'Blockchain'),
        ('E-commerce/Retail', 'E-commerce/Retail'),
        ('Fintech', 'Fintech'),
        ('Machine Learning/AI', 'Machine Learning/AI'),
        ('Robotic Process Automation', 'Robotic Process Automation'),
        ('Web', 'Web'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    scores = models.IntegerField(default=0)
    
    image = models.ImageField(upload_to='profiles', blank=True, default=None)
    backImage = models.ImageField(upload_to='back_images', blank=True, default=None)
    
    bio = RichTextField(max_length=500, blank=True)
    location = models.CharField(max_length=168, blank=True)
    
    Twitter = models.CharField(max_length=1000, blank=True)
    GitHub = models.CharField(max_length=1000, blank=True)
    GitLub = models.CharField(max_length=1000, blank=True) 
    Linkedin = models.CharField(max_length=1000, blank=True)
    Telegram = models.CharField(max_length=1000, blank=True)
    website = models.URLField(blank=True)
    
    # skills = MultiSelectField(choices=SKILLS, max_length=100, null=True, blank=True)
    # interests = MultiSelectField(choices=INTERESTS, max_length=100, null=True, blank=True)

    skills = models.ManyToManyField(Skill, blank=True, null=True)
    interests = models.ManyToManyField(Interest, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username