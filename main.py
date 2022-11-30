from typing import Union

from fastapi import FastAPI, Request

from sse_starlette.sse import EventSourceResponse

import json
import asyncio
import random

app = FastAPI()

quote = [
    ["Private capitalism makes a steam engine; State capitalism makes pyramids.", "Frank Chodorov"],
    ["The self-esteem of ignorance ignores wisdom." "Wesley D'Amico"],
    ["Regrets are mortal wounds.", "Dianne Marie Teresa Cole"],
    ["United we stand, disunited we die.", "Wesley D'Amico"],
    ["If the boat is going to sink, there is no point in patching the hull.", "Wesley D'Amico"],
    ["The roads of the past do not lead to the future.", "Wesley D'Amico"],
    ["I don't know what the bullshit is, but in dog fights, cats don't enter.", "Wesley D'Amico"],
    ["Passenger things do not update consciousness.", "Wesley D'Amico"],
    ["One thing i hate about being smart is that you notice everything even when someone is trying to fool you.", "Mackson Shaai"],
    ["Selfish children are just doing what they were taught!", "JAMES THOMAS"],
    ["Leadership is the art of getting someone else to do something you want done because he wants to do it.", "Dwight D. Eisenhower"],
    ["The secondary purpose of sport is to distract people from reality, it is the new drug of our generation.", "Mwanandeke Kindembo"],
    ["New trends will always shake us from left to right, as long as we don't know ourselves, like a pendulum swing.", "Mwanandeke Kindembo"],
    ["If your country wins the world cup, then the honour goes to your country and all the money to those who made it possible.", "Mwanandeke Kindembo"],
    ["Death means that life, or the soul, saying goodbye to the body; but that does not mean that life will not continue on different planes.", "Mwanandeke Kindembo"],
    ["We try so hard to create God in our image, instead of accepting the reality, that God is everything.", "Mwanandeke Kindembo"],
    ["Only a stubborn and unshakeable will-power can reach its final destination.", "Mwanandeke Kindembo"],
    ["The will-power of all great leaders is so close to that of the devil himself. But they are still humans at the end of the day.", "Mwanandeke Kindembo"],
    ["A mistake repeated more than once is a decision.", "Paulo Coelho"],
    ["The more you know, the less you need to say.", "Jim Rohn"],
    ["A free conscience is not bound by its own opinion.", "Wesley D'Amico"],
    ["The most painful thing is losing yourself in the process of loving someone too much, and forgetting that you are special too.", "Ernest Hemingway"],
    ["Perhaps the biggest mistake I made in the past was that I believed love was about finding the right person. In reality, love is about becoming the right person. Don’t look for the person you want to spend the rest of your life with. Become the person you want to spend your life with.", "Neil Strauss"],
    ["And now that the legislators and do-gooders have so futilely inflicted so many systems upon society, may they finally end where they should have begun: May they reject all systems, and try liberty; for liberty is an acknowledgment of faith in God and His works.", "Frederic Bastiat"],
    ["False is the idea of utility that sacrifices a thousand real advantages for one imaginary or trifling inconvenience; that would take fire from men because it burns, and water because one may drown in it; that has no remedy for evils except destruction.", "Cesare Beccaria"],
    ["I would rather starve and rot and keep the privilege of speaking the truth as I see it, than of holding all the offices that capital has to give from the presidency down.", "Henry Brooks Adams"],
    ["Live life and die, we will all die at a point.", "STHEMZA SA"],
    ["The best way to keep a prisoner from escaping is to make sure he never knows he’s in prison.", "Fyodor Dostoevsky"],
    ["A man who lies to himself, and believes his own lies becomes unable to recognize the truth, either in himself or anyone else, and he ends up losing respect for himself and others. When he had no respect for anyone, he can no longer love, and, in order to divert himself, having no love in him, he yields to his impulses, indulges in the lowest forms of pleasure, and behaves in the end like an animal. And it all comes from lying - to others and to yourself.", "Fyodor Dostoevsky"],
    ["Nothing in this world is harder than speaking the truth, nothing easier than flattery.", "Fyodor Dostoevsky"],
    ["Tolerance will reach such a level that intelligent people will be banned from thinking so as not to offend the imbeciles.", "Fyodor Dostoevsky"],
    ["To be a hero you need attitude, not fantasy.", "Wesley D'Amico"],
    ["It is the attitude that makes the hero, not the costume.", "Wesley D'Amico"],
    ["Know the rules well, so you can break them effectively.", "Dalai lama"],
    ["The goal is not to be better than the other man, but your previous self.", "Dalai lama"],
    ["Death carries no luggage.", "Wesley D'Amico"],
    ["Sometimes life sucks . . . get use to it.", "Tom Zegan"],
    ["Time doesn't wear a clock.", "Wesley D'Amico"],
    ["Where there is no contradiction, there is no conflict. see identification, concepts, relativity, epistemology.", "Michael Thais"],
    ["The dreamy slug gets wings, the pessimistic caterpillar will never fly.", "Wesley D'Amico"],
    ["If you pinch the sea of its liberty, though it be walls of stone or brass, it will beat them down.", "John Cotton"],
    ["Your book is dedicated by the soundest reason. You had better get out of France as quickly as you can.", "Voltaire"],
    ["If a single writer in a country is in chains, then there are some links of that chain that binds us all.", "Vaclav Havel"],
    ["Suppression of expression conceals the real problems confronting a society and diverts public attention from the critical issues. It is likely to result in neglect of the grievances which are the actual basis of the unrest, and this prevent their correction.", "Thomas I. Emerson"],
    ["Comrades, I consider it completely unimportant who in the party will vote, or how. But what is extraordinarily important is this: who will count the votes, and how.", "Josef Stalin"],
    ["Our experience has shown us that in the excitement of great popular elections, deciding the policy of the country, and its vast patronage, frauds will be committed, if a chance is given for them. If these frauds are allowed, the result is not only that the popular will may be defeated, and the result falsified, but that the worst side will prevail. The side which has the greater number of dishonest men will poll the most votes. The war cry, Vote early and vote often! and the familiar problem, how to cast the greatest number of votes with the smallest number of voters, indicate the direction in which the dangers lie.", "Richard Henry Dana, Jr."],
    ["I don't care who does the electing, so long as I get to do the nominating.", "William Marcy Tweed"],
    ["As you become more intimate with your suffering, your heart grows tender.", "Jack Kornfield"],
    ["Let go of the battle. Breathe quietly and let it be. Let your body relax and your heart soften. Open to whatever you experience without fighting.", "Jack Kornfield"],
    ["Acceptance is not passivity. It is a courageous step in the process of transformation.", "Jack Kornfield"],
    ["Everything that has a beginning has an ending. Make your peace with that and all will be well.", "Jack Kornfield"],
    ["Being on a spiritual path does not prevent you from facing times of darkness. But it teaches you how to use the darkness as a tool to grow.", "Jack Kornfield"],
    ["Love in the past is a memory. Love in the future is a fantasy. To be really alive, love – or any other experience – must take place in the present.", "Jack Kornfield"],
    ["The present moment is really all that we have. The only place you can really love another person is in the present.", "Jack Kornfield"],
    ["The things that matter most in our lives are not fantastic or grand. They are the moments when we touch one another.", "Jack Kornfield"],
    ["The heart is like a garden. It can grow compassion or fear, resentment or love. What seeds will you plant there?", "Jack Kornfield"],
    ["To let go does not mean to get rid of. To let go means to let be. When we let be with compassion, things come and go on their own.", "Jack Kornfield"],
    ["Anybody can manage order, a true master manages chaos.", "Jukka Mäki-Turja"],
    ["Children are permanently impressed only by the loyalties of their adult associates; precept or even example is not lastingly influential. Loyal persons are growing persons, and growth is an impressive and inspiring reality. Live loyally today—grow—and tomorrow will attend to itself. The quickest way for a tadpole to become a frog is to live loyally each moment as a tadpole.", "Melchizedek"],
    ["Kari Lake sounds off after being projected to lose gov race: ‘Arizonans know BS when they see it’", "Kari Lake"],
    ["Stupidity is not an infection, it’s a condition.", "Dianne Marie Teresa Cole"],
    ["My parents exhausted universal power in first creating me and then in naming me. They created for me an identity whether I wanted one or not.", "Scott C. Holstad"],
    ["Strangers frighten me. They remind me of you. Blood spills into the tub. Cramped quarters. Essence of fire. And garlic. Sweaty palms and images of the Diva rock me. Is it too late? Is it? Strangers frighten me. I dance puppet steps killing me hundreds of times over and over; I have a sickness to battle with you always there waiting.", "Scott C. Holstad"],
    ["chain link heat, a little over whelming some times when the sweat runs down your body like so many open veins jagged and throbbing", "Scott C. Holstad"],
    ["My plans for tomorrow is to be happy today.", "Wesley D'Amico"],
    ["Why won't God give me all of his power? Because he's afraid I might do good with it.", "Ryan Pack"],
    ["History always repeats itself,the first time as a tragedy and then again as a farce.", "Tjatjitua Tjiyahura"],
    ["I met this Oscar-winning director at a party in Beverly Hills and everyone got mad at me because I didn’t know who he was. Well, he didn’t know who I was either so I guess it evened out. Still, I could hear them muttering Holstad can’t write anyway, I liked him more when he wrote funny poems so I went home, wrote this poem, drank some Jack straight up and threw away the director’s video that my wife had been given.", "Scott C. Holstad"],
    ["So little of what we observe is Actuality. Do we see/hear the words pouring forth? Are they Truth? I wish and hope but my future is predestined per my parents’ belief and that is denial and death, the deepest pits of hell, the thorniest of crowns, no sympathy, simply guilt, pain, anguish and lament. Call me your Anti-Savior and I’ll take on your pain too.", "Scott C. Holstad"],
    ["Websites that collect quotes are full of mistakes and never check original sources.", "Randal Monroe"],
    ["We don’t live in our fears, we live in our hopes.", "Mike Tomlin"],
    ["The one thing you learn is when you can step out of your comfort zone and be uncomfortable you see what you’re made of and who you are.", "Sue Bird"],
    ["If you can dream it, you can do it.", "Enzo Ferrari"],
    ["The inability of a state body to accept factual criticism and to make amends should worry every Israeli citizen.", "Bezalel Smotrich"],
    ["There is great beauty in each season, but autumn has a touch of something more.", "Laura Jaworski"],
    ["The tsunami was announced and those who didn't believe it went to the beach to see it.", "Wesley D'Amico"],
    ["I prefer dangerous freedom over peaceful slavery.", "Thomas Jefferson"],
    ["Autumn when the trees shake loose their garments and we bundle in our own.", "Laura Jaworski"],
    ["Nothing's forgotten. Nothing is ever forgotten.", "Robin Hood"],
    ["Autumn is a place where words fall short. It is a magic that must be felt, breathed, experienced, and treasured.", "Laura Jaworski"],
    ["If life were predictable it would cease to be life, and be without flavor.", "Eleanor Roosevelt"],
    ["making peace with people is the only wat yo success", "Tallulah Bankhead"],
    ["Each peaceful breath is a petal opening on the bud of humanity, a bloom on the flower of life.", "Laura Jaworski"],
    ["don't aspire to be the best on the team, but aspire to be the best for the team.", "Rudyard Kipling"],
    ["Sometimes to get what you want the most, you have to do what you want the least. Jodi Picoult", "Jodi Picoult"],
    ["They race from us! Only to find us sooner.", "Kindred, League of Legends"],
    ["If what you think is right seems wrong, there must be something wrong with what you think is right", "William Sloane Coffin"],
    ["Some parts of the Arab sector do not understand that this is the state of Israel and this is a Jewish state.", "Itamar Ben Gvir"],
    ["In every place they want to evacuate Jews, there will be a struggle.", "Itamar Ben Gvir"],
    ["When you have no political home, you have no power.", "Itamar Ben Gvir"],
    ["The number one reason people fail in life is because they listen to their friends, family, and neighbors.", "Napoleon Hill"],
    ["What's behind you doesn't matter.", "Enzo Ferrari"],
    ["There is always someone out there getting better than you by training harder than you.", "Pele"],
    ["I learned to fly by watching the birds.", "Wesley D'Amico"],
    ["We must have the courage to turn against our habitual lifestyle and engage in unconventional living." "Christopher McCandless"],
    ["The life and the simple beauty of it is too good to pass up.", "Christopher McCandless"],
    ["Don't hesitate or allow yourself to make excuses. Just get out and do it. Just get out and do it. You will be very, very glad that you did.", "Christopher McCandless"],
    ["I now walk into the wild.", "Christopher McCandless"],
    ["All true meaning resides in the personal relationship to a phenomenon, what it means to you.", "Christopher McCandless"],
    ["It is the experiences, the great triumphant joy of living to the fullest extent in which real meaning is found. God it's great to be alive!", "Christopher McCandless"],
]


@app.get('/oneSameQuote')
async def read_quote():
    return {"text": "Stay Hungry, Stay Foolish.", "author": "Steven Jobs"}


@app.get('/oneDifferentQuote')
async def read_quote():
    n = random.random() * 100
    return {"text": quote[int(n)][0], "author": quote[int(n)][1]}


@app.get('/manySameQuote')
async def read_quote():
    return [{"text": "Stay Hungry, Stay Foolish.", "author": "Steven Jobs"}, {"text": "Art is like life, unique.", "author": "Unknow"}]


@app.get('/manyDifferentQuote')
async def read_quote():
    n = random.random() * 100
    m = random.random() * 100
    return [{"text": quote[int(n)][0], "author": quote[int(n)][1]}, {"text": quote[int(m)][0], "author": quote[int(m)][1]}]


STREAM_DELAY = 1  # second
RETRY_TIMEOUT = 15000  # milisecond

@app.get('/stream/oneSameQuote')
async def message_stream(request: Request):
    def new_messages():
        # Add logic here to check for new messages
        yield 'Hello World'
    async def event_generator():
        while True:
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                break

            # Checks for new messages and return them to client if any
            if new_messages():
                # yield {
                #         "event": "new_message",
                #         "id": "message_id",
                #         "retry": RETRY_TIMEOUT,
                #         "data": "Stay Hungry, Stay Foolish."
                # }
                yield json.dumps({"text": "Stay Hungry, Stay Foolish.", "author": "Steven Jobs"})

            await asyncio.sleep(STREAM_DELAY)

    return EventSourceResponse(event_generator())

@app.get('/stream/oneDifferentQuote')
async def message_stream(request: Request):
    def new_messages():
        # Add logic here to check for new messages
        yield 'Hello World'
    async def event_generator():
        while True:
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                break

            # Checks for new messages and return them to client if any
            if new_messages():
                # yield {
                #         "event": "new_message",
                #         "id": "message_id",
                #         "retry": RETRY_TIMEOUT,
                #         "data": "Stay Hungry, Stay Foolish."
                # }
                n = random.random() * 100
                yield json.dumps({"text": quote[int(n)][0], "author": quote[int(n)][1]})

            await asyncio.sleep(STREAM_DELAY)

    return EventSourceResponse(event_generator())

@app.get('/stream/manySameQuote')
async def message_stream(request: Request):
    def new_messages():
        # Add logic here to check for new messages
        yield 'Hello World'
    async def event_generator():
        while True:
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                break

            # Checks for new messages and return them to client if any
            if new_messages():
                # yield {
                #         "event": "new_message",
                #         "id": "message_id",
                #         "retry": RETRY_TIMEOUT,
                #         "data": "Stay Hungry, Stay Foolish."
                # }
                yield json.dumps([{"text": "Stay Hungry, Stay Foolish.", "author": "Steven Jobs"}, {"text": "Art is like life, unique.", "author": "Unknow"}])

            await asyncio.sleep(STREAM_DELAY)

    return EventSourceResponse(event_generator())

@app.get('/stream/manyDifferentQuote')
async def message_stream(request: Request):
    def new_messages():
        # Add logic here to check for new messages
        yield 'Hello World'
    async def event_generator():
        while True:
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                break

            # Checks for new messages and return them to client if any
            if new_messages():
                # yield {
                #         "event": "new_message",
                #         "id": "message_id",
                #         "retry": RETRY_TIMEOUT,
                #         "data": "Stay Hungry, Stay Foolish."
                # }
                n = random.random() * 100
                m = random.random() * 100
                yield json.dumps([{"text": quote[int(n)][0], "author": quote[int(n)][1]}, {"text": quote[int(m)][0], "author": quote[int(m)][1]}])

            await asyncio.sleep(STREAM_DELAY)

    return EventSourceResponse(event_generator())
