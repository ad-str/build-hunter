from django.db import models
from django.core.exceptions import ValidationError

class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)
    max_level = models.IntegerField(choices=[(i, i) for i in range(1, 8)])
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_skill_name')
        ]
    

class Decoration(models.Model):
    name = models.CharField(max_length=255, unique=True)
    size = models.IntegerField(choices=[(i, i) for i in range(1, 5)])
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    skill_level = models.IntegerField()

    def __str__(self):
        return f"{self.name}: {self.skill.name} Lv. {self.skill_level}"
    
    def clean(self):
        if self.skill_level < 1 or self.skill_level > self.skill.max_level:
            raise ValidationError({
                'skill_level': 'Skill level cannot be more than skill\'s max level.'
            })


    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_decoration_name')
        ]

class Armor(models.Model):
    ARMOR_CATEGORIES = {
        'head': "Head",
        'chest': "Chest",
        'arm': "Arm",
        'waist': "Waist",
        'leg': "Leg"
    }
    category = models.CharField(max_length=5, choices=ARMOR_CATEGORIES)
    name = models.CharField(max_length=255, unique=True)
    skills = models.ManyToManyField(Skill, through='ArmorSkill')
    slot1 = models.IntegerField(choices=[(i, i) for i in range(0, 5)])
    slot2 = models.IntegerField(choices=[(i, i) for i in range(0, 5)])
    slot3 = models.IntegerField(choices=[(i, i) for i in range(0, 5)])
    defense = models.IntegerField()
    fire_res = models.IntegerField()
    water_res = models.IntegerField()
    thunder_res = models.IntegerField()
    ice_res = models.IntegerField()
    dragon_res = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.category})"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_armor_name')
        ]

class ArmorSkill(models.Model):
    armor = models.ForeignKey(Armor, on_delete=models.CASCADE, related_name="armors")
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="skills")
    level = models.IntegerField()

    def clean(self):
        # Custom validation logic
        if self.level < 1 or self.level > self.skill.max_level:
            raise ValidationError({
                'skill_level': 'Skill level cannot be more than skill\'s max level.'
            })

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.armor.name}-{self.skill.name} Lv, {self.level}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['armor', 'skill'], name='unique_armor_skill')
        ]
