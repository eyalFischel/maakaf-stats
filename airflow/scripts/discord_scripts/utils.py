
def is_projects_category(category):
    return category.name.lower().startswith('projects-')

def is_text_channel(channel):
    return channel.type.value == 0

def update_member_activity(message, member_activity):
    author = message.author
    channel = message.channel

    if author.name not in member_activity:
        member_activity[author.name] = {}
    
    if channel.name not in member_activity[author.name]:
        member_activity[author.name][channel.name] = [0, 0]
    
    member_activity[author.name][channel.name][0] += 1
    member_activity[author.name][channel.name][1] = message.created_at.strftime('%Y-%m-%d %H:%M:%S')
    print(f'member activity: {member_activity}')

def update_project_activity(message, project_activity):
    channel_name = message.channel.name
    created_at = message.created_at

    if channel_name not in project_activity:
        project_activity[channel_name] = [0, 0]
    
    project_activity[channel_name][0] += 1
    project_activity[channel_name][1] = created_at.strftime('%Y-%m-%d %H:%M:%S')
    print(f'project activity: {project_activity}')
