from Tag import Tag, WikipediaArticle

users = {}
idleUsers = {}

class User:
    users = {}
    idleUsers = {}

    def __init__(self, name, pwd):
        self.name = name
        self.pwd = pwd
        self.ip = ''
        self.tags = set()
        self.karma = 100.0
        self.socket = 0

    def upVote(self, target):
        """
        Allows a user to increase the karma of another user. The amount of
        influence (the affect they have on another user's karma) is directly
        related to the karma of the voter.
        Takes one argument of type User.
        """
        target.karma += 5*self.karma/100

    def downVote(self, target):
        """
        Allows a user to decrease the karma of another user. Like upVote,
        the amount of influence the voter has is directly related to the
        voter's karma.
        Takes one argument of type User.
        """
        target.karma -= 5*self.karma/100

    def addTag(self, tag):
        """
        Adds an interest tag (ie. "physics" or "dogs") to a user's list of
        interests.
        Takes one argument of type Tag.
        """
        self.tags.add(Tag(tag))

    def removeTag(self, tag):
        """
        Removes an interest tag from the user's interest list.
        Takes one argument of type Tag.
        """
        try:
            self.tags.remove(tag)
        except KeyError as e:
            print("You don't have that tag!")

    def tagMatch(self, user):
        '''
        Calculates the "match score" (arbitrary ranking system) based on
        similarities of two Users' interests.
        Takes one argument of type User.
        '''
        points = 0
        similarities = 0
        for self_tag in self.tags:
            for other_tag in user.tags:
                similarity = self_tag.similarityTo(other_tag)
                if similarity > 0.5:
                    similarities += 1
                    points += similarity
        return points/similarities

    def karmaMatch(self, user):
        """
        Calculates the "match score" based on the similarities of two Users'
        karma points. This is to ensure that the well behaved Users are
        rewarded by getting matched with a generally more well behaved
        user base that one person who is less liked.
        Takes one argument of type User.
        """
        score = 3*(1/100)*(abs(self.karma - user.karma))
        if score <= 0:
            return 0
        else:
            return score

    def compatibility(self, user):
        """
        Combines the match scores of the two users and returns the final
        "compatibility score."
        Takes one argument of type User.
        """
        return self.tagMatch(user)+self.karmaMatch(user)



def findMatch(client):
    """
    Method used by the server to find the best match for a client. Returns
    the User with the best match score of the client.
    Takes one argument of type User.
    """
    maxscore = 0
    bestmatch = None
    for user in idleUsers:
        if client.name != user.name:
            score = client.compatibility(user)
            if score > maxscore:
                maxscore = score
                bestmatch = user
    return bestmatch

def findFromSocket(socket):
    """
    Returns a user based on the socket number.
    Takes one argument of type Socket.
    """
    for user in User.users:
        if user.socket == socket:
            return user

def findFromIP(ip):
    """
    Retures a user based on the IP number
    Takes one argument of type String
    """
    for user in User.users:
        if user.ip == ip:
            return user

def addUser(user):
    """
    Adds a user to the list of active users.
    Takes one argument of type User.
    """
    User.users.add(user)

def addIdleUser(user):
    """
    Adds a user to the list of inactive users.
    Takes one argument of type User.
    """
    User.idleUsers.add(user)

def removeIdleUser(user):
    """
    Removes a User from the list of inactive users.
    Takes one argument of type User.
    """
    User.idleUsers.remove(user)
