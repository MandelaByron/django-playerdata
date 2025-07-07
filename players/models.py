from django.db import models
from django.urls import reverse
class Player(models.Model):

    id = models.IntegerField(primary_key=True)
    
    name = models.CharField(max_length=250)
    
    age = models.IntegerField(null=True)
    
    jersey_number = models.IntegerField(null=True)
    
    place_of_birth = models.CharField(max_length=250, null=True)
    place_of_birth_title = models.CharField(max_length=250, null=True)
    place_of_birth_flag = models.URLField(null=True)
    date_of_birth = models.DateField(null=True)
    height = models.FloatField(null=True)
    foot = models.CharField(null=True, max_length=10)
    citizenship = models.JSONField(null=True)
    citizenship_flag = models.JSONField(null=True)
    headshot = models.URLField(null=True)
    
    club = models.CharField(max_length=100)
    
    club_logo = models.URLField(null=True, max_length=250)
    
    main_position = models.CharField(null=True)
    
    other_positions = models.JSONField(null=True)
    
    national_team = models.CharField(null=True)
    
    national_team_flag = models.URLField(null=True)
    
    caps = models.IntegerField(null=True)
    
    international_goals = models.IntegerField(null=True)
    
    market_value = models.IntegerField(null=True)
    
    league_name = models.CharField(max_length=100, null=True)
    
    league_level = models.CharField(max_length=100, null=True)
    
    league_logo = models.URLField(null=True, max_length=250)
    
    joined_date = models.DateField(null=True)
    
    contract_expires = models.DateField(null=True)
    
    agency_info = models.JSONField(null=True)
    
    club_stats = models.JSONField(null=True)
    
    national_team_stats = models.JSONField(null=True)
    
    current_season_stats = models.JSONField(null=True)
    
    class Meta:
        
        ordering = [
            models.F("market_value").desc(nulls_last=True),
            models.F("caps").desc(nulls_last=True),
        ]
        
        indexes = [
            models.Index(fields=['id', "market_value"])
        ]
        
    def __str__(self) -> str:
        return f"{self.name} - {self.id}"
    
    def get_absolute_url(self):
        return reverse("player-detail", kwargs={"id": self.id})
    
    @property
    def club_logo_head(self):
        return self.club_logo.replace('small', 'head')
    
    @property
    def formatted_market_value(self):
        value = self.market_value
        if value >= 1_000_000_000:
            return f"€{value // 1_000_000_000}b"
        elif value >= 1_000_000:
            return f"€{value // 1_000_000}m"
        elif value >= 1_000:
            return f"€{value // 1_000}k"
        else:
            return f"€{value}"
        
        #June 27, 2023

    @property
    def first_national_team_debut(self):
        debut_list = self.national_team_stats.get("debut") if self.national_team_stats else []
        return debut_list[0] if debut_list else None
    
    @property
    def second_nationality(self):
        """Returns a tuple: (flag_url, country_name) or None"""
        if not self.citizenship or not self.citizenship_flag:
            return None

        # Ensure both are lists
        countries = self.citizenship if isinstance(self.citizenship, list) else [self.citizenship]
        flags = self.citizenship_flag if isinstance(self.citizenship_flag, list) else [self.citizenship_flag]

        # Return 2nd if available
        if len(countries) > 1 and len(flags) > 1:
            return (flags[1], countries[1])
        return None
    

    


