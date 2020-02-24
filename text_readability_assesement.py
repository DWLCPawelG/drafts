import textstat

text = """
The need to push through with this initiative was born from daily frustrations and failures in understanding features written as tickets on Jira. Some are good enough, others aren't, but the goal is to set and keep a standard in documentation procedures that will enhance readability, reduce time & effort expenses required to understand and process new functionalities.
​
Our target is to make Jira User Stories (but also Bugs/Epics/Tasks and so on) as clear and comprehensible as they can be to everyone involved.
​
You won't find anything revolutionary here, because the problem does not require any innovation - if we all stick to the basics, we should do just fine.
The Solution
​
The Perfect Jira Ticket (let me know if you ever see one)
​
A ticket has to provide enough information for anyone to understand it - it's much easier in User Stories than Tasks/Bugs which often contain more detailed info on software behaviour. Be sure to fill out the following fields accordingly:
Summary - that depends on the type of ticket, but all of them share the same qualities. They should be clear, concrete, and (if possible) short. The summary is your headline - if it doesn't attract the reader, that means the Project loses.
Description - it's always desired that the ticket description is short but don't hold back in putting in anything you might find useful or state the obvious - what may be clear as day to you, may not to someone else. Remember that Perception Is Not Reality.
Attachments - if there are any documents describing the feature accepted by the client, feel free to insert them here or add links to documentation on Google Drive, Confluence, etc.
​
Also, be sure to squeeze Acceptance Criteria or Definition of Done in there somewhere - these are essential (more than that in the next paragraph). If a ticket has all the required ingredients that's a win - the assignee is able to start dealing with the problem without any obstructions.
​
​
Put emphasis on documenting Acceptance Criteria
​
Although Jira is no place for essays, it is more than possible to pass enough info on a subject in a structured way. This is not the place for software development definitions, you can read about well-defined ACs here or here or here  or on a zillion other websites.. What is essential though is to document them.
​
When discovering a new business requirement, both the Development and QA Team need to know as much as possible on the client's demands. Well-defined Acceptance Criteria can be a catalyst for creative solutions, new concepts of development and different approaches in testing.
​
​
Reference to existing outside documentation
​
As we all know there are thousands of emails, documents, spreadsheets and files circulating within our company every day. Some of them contain correspondence with our clients and hold valuable information on their requirements. These get transformed by Product Owners/Project Owners/Solution Architects/Backlog Owners to Jira User Stories and often get lost in the shuffle. Then comes the dreaded 'Blocker' - a misunderstanding of client's demands that disrupts the whole working process.
​
We've all been there. Digging through hundreds of documents in search of that one phrase holding the answer can be frustrating and time-consuming. So why not save ourselves the fuss and link any documentation/email threads to a User Story/Epic/Bug? After all, if it's not confidential than what's the point of not exposing all info to those assigned to deliver the product?
​
​
Comments section as a Forum
​
All things are subject to change - business requirements are no exception to that. When they do so, all reference documentation should also be updated but that's not always the case. Sometimes in our work, we come across outdated documentation or mutually exclusive requirements. It's vital we keep better track of any changes in the project documentation. Changes initiated by any side - be it client, dev team, sales department or other, should be consulted with all interested parties, thoroughly documented and then delivered asap in written form. 
​
Slack/Skype/WebEx is great but why not share your knowledge with everybody? Use comments under tickets to express your concerns, ask questions, give answers or share interesting findings on a given subject. Don't keep the knowledge to yourself, share it around for the benefit of anyone interested.
​
​
Overcome the communication barrier
​
We have the opportunity to work in an international company with employees across three(?) continents. That raises challenges such as: location - people collaborate on the same projects without seeing each other eye-to-eye on a daily basis, or never even met in person, English proficiency, staff rotation - new people join in on our journey every month and their onboarding takes time, the complexity of the issue - the IoT subject we deal in is a tough nut to crack both in terms of concept and vocabulary.
​
Taking all these factors into consideration, we face a huge task of getting on the same page if we are to achieve our goals. To tackle this, let's stick to principles of written communication. You can find hundreds of guidelines online on how to communicate efficiently with writing (I like this one, it hits the nail on the head). Remember that the foundation of all communication is being able to make the other side understand your thoughts and intentions - so be as basic and direct as you can.
​
Use simple words, avoid going into code language details if not absolutely necessary (especially if the ticket will be processed outside of your team which is familiar with the topic), link any definitions and nuances you're introducing. Let's make sure our internal documentation is as easy to absorb by anyone.
​
​
Broader usages of Feedback and Blocked statues
​
No one likes to be ignored. Lack of action is detrimental to the success of the project and ultimately bad for business. We would like to propose introducing Feedback and Blocked statuses on Jira Boards where these are missing and encourage to use them when you feel it is necessary. In PDM (always in our hearts), usage of these statuses was common and had a positive impact.
​
PDM Bugs Workflow
​
If a ticket Summary, Description, Steps to Reproduce or Expected Result are not clear enough for you, use the Feedback status and assign it back to the previous assignee. Be sure to leave a comment describing what you require to proceed.
If you can't proceed with the resolution of the ticket because of any other limitations, set it to Blocked status and give your reasons for doing so in the Comments. Also, remember to change Assignee to whoever you think is responsible for unblocking the issue or the Project Manager if you don't know who that might be.
​
If you decide to do so, you will be able to track the time tickets spend in Feedback and Blocked statuses here. You can set a custom timespan, desired ticket status, and project to see how you're progressing. 
​
​
Company Glossary - a concept, TBD with Docs Team
​
Ever had the impression during a conversation that both of you are talking about the same thing but you name it differently? That's common in growing businesses like our company. For example, definition of a device varies, or what's a view to someone is a section to someone else. Or my favourite: some people even refer to bugs as features.
​
The list is very long. Many times the differences stem from the Project customization and it's not possible to have alerts when the client requested faults. But some of them can be unified. Enter the Docs Team! Our Technical Writers are working on a glossary of business, technical and other terms used in our company so that we make sure we're all on the same page in terms of vocabulary.
​
​
"""

print(textstat.syllable_count(text))
print(f"The Flesch Reading Ease score is: {textstat.flesch_reading_ease(text)}")
print(f"The Flesch-Kincaid Grade level is: {textstat.flesch_kincaid_grade(text)}")
print(f"The Dale-Chall Readability Score is: {textstat.dale_chall_readability_score(text)}")
print(f"The readability consensus is: {textstat.text_standard(text, float_output=False)}")
