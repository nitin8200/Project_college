from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tool(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tools')
    image = models.ImageField(upload_to='tools/')
    rating = models.FloatField(default=0.0)
    website_url = models.URLField()
    is_featured = models.BooleanField(default=False)
    pricing = models.CharField(
        max_length=50,
        choices=[
            ('Free', 'Free'),
            ('Freemium', 'Freemium'),
            ('Paid', 'Paid'),
            ('Subscription', 'Subscription'),
        ],
        default='Free'
    )
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags for the tool")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_tags_list(self):
        """Returns the tags as a list."""
        return [tag.strip() for tag in self.tags.split(',')] if self.tags else []

class Review(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='reviews')
    username = models.CharField(max_length=50)
    content = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.username} on {self.tool.name}"

class Comparison(models.Model):
    tool_1 = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='comparison_1')
    tool_2 = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='comparison_2')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tool_1.name} vs {self.tool_2.name}"




