from Tag import Tag, WikipediaArticle

Users = []
idleUsers = []

class User:
    def __init__(self, name, pwd):
        self.name = name
        self.pwd = pwd
        self.ip = ''
        self.tags = set()
        self.karma = 100.0
        self.socket = 0

    def upVote(self, target):
        target.karma += 5*self.karma

    def downVote(self, target):
        target.karma -= 5*self.karma
        if target.karma <= 1:
            target.karma = 1

    def addTag(self, tag):
        #Takes a string argument
        self.tags.add(Tag(tag))

    def removeTag(self, tag):
        #Takes a Tag argument
        try:
            self.tags.remove(tag)
        except KeyError as e:
            print("You don't have that tag!")

    def tagMatch(self, user):
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
        score = 3-(1/100)*(abs(self.karma - user.karma))
        if score <= 0:
            return 0
        else:
            return score

    def compatibility(self, user):
            return self.tagMatch(user)+self.karmaMatch(user)

def findMatch(client):
    maxscore = 0
    bestmatch = None
    for user in idleUsers:
        if client.name != user.name:
            score = client.compatibility(match)
            if score > maxscore:
                maxscore = score
                bestmatch = user
    return bestmatch

def findFromSocket(socket):
    for user in Users:
        if user.socket == socket:
            return user

def findFromIP(ip):
    for user in Users:
        if user.ip == ip:
            return user

def addUser(user):
    Users.append(user)

def addIdleUser(user):
    idleUsers.append(user)

def removeIdleUser(user):
    return 0
'''
#Testing
science = Tag('science')
physics = Tag('physics')
dog = Tag('dog')
cat = Tag('cat')
print("Testing if science is similar to physics")
print(science.similarityTo(physics))

rz = User('richie','123')
tejas = User('tejas','123')

rz.addTag('science')
rz.addTag('dog')
rz.upVote(tejas)
tejas.addTag('physics')
tejas.addTag('cat')
idleUsers.append(tejas)
print("Creating two users, richie and tejas")
print("Match points from related interests")
print(rz.tagMatch(tejas))
print("Match points from karma")
print(rz.karmaMatch(tejas))
print("Total compatibility")
print(rz.compatibility(tejas))
'''
print("Give interests for person1")
p1 = User('person1','123')
p1.addTag(raw_input())
p1.addTag(raw_input())
p1.addTag(raw_input())

print("Give interests for person2")
p2 = User('person2','123')
p2.addTag(raw_input())
p2.addTag(raw_input())
p2.addTag(raw_input())

print("Calculating compatibility...")
print(p1.compatibility(p2))
'''
#TESTING TAG COMPARISON
tag1 = raw_input()
tag2 = raw_input()
print("Testing compatibility...")
print(Tag(tag1).similarityTo(Tag(tag2)))
'''
