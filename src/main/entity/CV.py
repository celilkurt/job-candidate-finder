class CV:
    id: str
    skills: str
    experience: str
    education: str
    objective: str  # or summary
    date: str

    """
    Desired Industry
    Management
    SpiderID
    Desired Job Location
    Date Posted
    Type of Position
    Availability Date
    Desired Wage
    U.S. Work Authorization
    Job Level
    Willing to Travel
    Highest Degree Attained
    Willing to Relocate
    """
    # Affiliations


    def __init__(self, id='', skills='', experience='', education='', objective='', date=''):
        self.id = id
        self.skills = skills
        self.experience = experience
        self.education = education
        self.objective = objective
        self.date = date
