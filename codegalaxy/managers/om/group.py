import dbw
import managers.om.user
import managers.om.objectmanager
import datetime
import time
import markdown2

import os.path

markdown_converter = markdown2.Markdown()

# Object representation of an exerciselist
class Group:

    def __init__(self, id, group_name, group_type, created_on):
        '''
        @brief init of group
        @param id the if of the group
        @param group_name the name of the group
        @param group_type the type of the group
        @param created_on the date the group was created on
        '''
        self.id = int(id)
        self.group_name = group_name
        # private/public/...
        self.group_type = group_type
        self.created_on = created_on

    def name(self):
        return self.group_name

    # Returns the path to the picture associated with this group
    def getPicture(self):
        group_picture = "group_pictures/{}.png".format(self.id)
        path = "./codegalaxy/static/" + group_picture

        if os.path.isfile(path):
            group_picture = group_picture
        else:
            group_picture = "media/icons/group.png"
        return group_picture

    # deletes the group and thereby all th memberships aswell
    def disband(self):
        dbw.deleteGroupPosts(self.id)
        dbw.deleteGroup(self.id)

    # list of users that are member of this group
    def allMembers(self):
        '''
        @return get all the members of a group, if there are none return empty list
        '''
        members_infos = dbw.getUsersInGroup(self.id)
        object_manager = managers.om.objectmanager.ObjectManager()
        user_list = []
        for members_info in members_infos:
            user_list.append(object_manager.createUser(id=members_info['user_id']))
        return user_list

    # list of users that are not member of this group
    def allUsersNotMember(self):
        '''
        @return get all users that are not a member of this group, if there are none return empty list
        '''
        members_infos = dbw.getUsersNotMember(self.id)
        object_manager = managers.om.objectmanager.ObjectManager()
        user_list = []
        for members_info in members_infos:
            user_list.append(object_manager.createUser(id=members_info['id']))
        return user_list

    # Updates the database to the variables on the current object
    def save(self):
        '''
        @brief save a group object
        '''
        dbw.updateGroup(self.id, self.group_name, self.group_type, self.created_on)

    # Checks whether a user has been invited to join this group
    def membershipPending(self, user_id):
        pending_group_memberships = dbw.getPendingGroupMemberships(user_id)

        for pending_group_membership in pending_group_memberships:
            if pending_group_membership['group_id'] == self.id:
                if pending_group_membership['user_id'] == user_id:
                    return True
        return False

    # Adds a new member to the group
    def insertMember(self, user_id, user_permissions, joined_on, status):
        '''
        @brief inserts a member in the group
        @param user_id the id of the user
        @param user_permissions the permissions of the user in this group
        @param joined_on the date the user joined on
        '''
        dbw.insertUserInGroup(self.id, user_id, user_permissions, joined_on, status)
        if status == 'Member':
            dbw.incrementBadgeValue(user_id, 'memberOfGroup')

    # Removes a member from the group
    def deleteMember(self, user_id):
        dbw.deleteUserFromGroup(self.id, user_id)
        dbw.decrementBadgeValue(user_id, 'memberOfGroup')

    # Checks the permissions of a certain user (member, admin, owner)
    def getUserPermissions(self, user_id):
        permissions = dbw.getGroupUserPermissions(self.id, user_id)
        return int(permissions[0]['user_permissions'])

    # Changes the permissions for auser in this group
    def upgradeUserPermissions(self, user_id):
        # 0 = OWNER, 1 = ADMIN, 2 = USER
        dbw.updateUserPermissions(self.id, user_id, 1)

    # Wordt gebruikt om een dictionarry te maken van zoekresultaten
    def searchString(self):
        return str(self.group_name)

    # De HTML code die door JQuery na een Ajax call gebruikt wordt bij het zoeken naar user/group
    def searchResult(self, cur_user):
        group_owner = ''
        friends_in_group = ' | '
        for friend in cur_user.allFriends():
            for member in self.allMembers():
                if self.getUserPermissions(member.id) == 0:
                    group_owner = member.name()
                if friend.id == member.id:
                    friends_in_group += friend.name() + ' | '

        if len(friends_in_group) < 5:
            result = '''
            <div class="large-12 columns end">
              <div class="panel radius">
                <div class="row">
                  <div class="large-3 columns">
                    <a href="/g/{id}">
                      <img src="/static/{picture}" class="round-image"/>
                    </a>
                  </div>
                  <div class="large-9 columns left">
                    <div class="row">
                      <a href="/g/{id}">
                        <h5 class="text-cut-off"><b>{name}</b> ({nr_of_members} members)</h5>
                      </a>
                    </div>
                    <br>
                    <br>
                    <div class="row">
                      <a href="/g/{id}">
                        <h6 class="text-cut-off"><b>Owner:</b> {owner}</h6>
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            '''.format(id=self.id, picture=self.getPicture(), nr_of_members=len(self.allMembers()), name=self.name(), owner=group_owner)

            return result

        result = '''
        <div class="large-12 columns end">
          <div class="panel radius">
            <div class="row">
              <div class="large-3 columns">
                <a href="/g/{id}">
                  <img src="/static/{picture}" class="round-image"/>
                </a>
              </div>
              <div class="large-9 columns left">
                <div class="row">
                  <a href="/g/{id}">
                    <h5 class="text-cut-off"><b>{name}</b> ({nr_of_members} members)</h5>
                  </a>
                </div>
                <br>
                <div class="row">
                  <a href="/g/{id}">
                    <h6 class="text-cut-off"><b>Owner:</b> {owner}</h6>
                  </a>
                </div>
                <div class="row">
                  <a href="/g/{id}">
                    <h6><b>Friends in group:</b> {friends_in_this_group}</h6>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
        '''.format(id=self.id, picture=self.getPicture(), nr_of_members=len(self.allMembers()), name=self.name(), owner=group_owner, friends_in_this_group=friends_in_group)

        return result

    def __str__(self):
        '''
        @brief string representation of the group
        '''
        return str(self.id) + ' ' + self.group_name + ' ' + str(self.group_type) + " " + str(self.created_on)

    # Adds a new post to the group's wall
    def postOnWall(self, user_id, text):
        last_post_id = dbw.lastPostID()['last']
        if last_post_id is None:
            last_post_id = 0
        dbw.insertPost(self.id, user_id, last_post_id + 1, 0, text, str(time.strftime("%Y-%m-%d %H:%M:%S")))

    # Deletes a post from the group's wall
    def deletePost(self, post_id):
        # we'll need to delete the replies aswell -> recursion
        replies_to_post = []
        # getting the replies to this post
        for reply in replies_to_post:
            self.deletePost(reply)
        dbw.deletePost(post_id)

    # Edits a post on the group's wall
    def editPost(self, post_id, text):
        dbw.updatePost(post_id, text)

    # Returns all the posts on the group's wall
    def allPosts(self):
        posts = []
        posts_info = dbw.getAllPostsForGroup(self.id)
        for info in posts_info:
            posts.append(Post(info['id'], info['group_id'], info['user_id'],
            info['reply'], info['reply_number'], info['post_text'],
                info['posted_on']))
        posts.sort(key=lambda x: x.posted_on, reverse=True)
        return posts

    # Returns all the posts on this group's wall, converted to html (for the group.html page)
    def allPostsToHTML(self, logged_user):
        html = ''
        all_posts = self.allPosts()
        original_posts = []
        for post in all_posts:
            if post.id == post.reply:
                original_posts.append(post)
        for post in original_posts:
            html += post.HTMLString(logged_user)
        return html

# Object representation of a post
class Post:

    def __init__(self, id, group_id, user_id, reply, reply_number, post_text, posted_on):
        '''
            reply is which it refers to,if it's the first one
            it refers to itself
        '''

        self.id = int(id)
        self.group_id = int(group_id)
        self.user_id = int(user_id)
        self.reply = int(reply)
        self.reply_number = int(reply_number)
        self.post_text = post_text.decode('utf-8')
        self.posted_on = posted_on
        self.object_manager = managers.om.objectmanager.ObjectManager()

    def __str__(self):
        return str(self.id) + ' \n' + str(self.group_id) + ' \n' + str(self.user_id) + ' \n' + str(self.reply) + ' \n' + str(self.reply_number) + ' \n' + self.post_text + '\n\n'

    # Post deletes itself from the database
    def delete(self):
        for reply in self.allReplies():
            if reply.id != self.id:
                reply.delete()
        dbw.deletePost(self.id)

    # Updates the database to the variables on the current object
    def save(self):
        dbw.updatePost(self.id, self.post_text)

    # Reply to this post
    def replyToPost(self, user_id, text):
        last_reply_number = dbw.lastReplyToPost(self.id)['last']
        if not last_reply_number:
            last_reply_number = 0
        dbw.insertPost(self.group_id, user_id, self.id, last_reply_number, text, str(time.strftime("%Y-%m-%d %H:%M:%S")))

    # Returns all the replies to this post
    def allReplies(self):
        replies = []
        replies_info = dbw.getAllRepliesToPost(self.id)
        for info in replies_info:
            if info['id'] != self.id:
                replies.append(Post(info['id'], info['group_id'], info['user_id'],
                                    info['reply'], info['reply_number'], info['post_text'],
                                    info['posted_on']))
        replies.sort(key=lambda x: x.reply_number, reverse=True)
        return replies

    # Adds html data (posts id)
    def addPostDataVariables(self):
        html = ' data-post_id=' + str(self.id)
        return html

    # html representation (with markdown) of a a part of a post/reply
    def HTMLBasic(self, user, logged_user):
        html = '''
        <div class="post_text">
            {text}
        </div>
        <p class="timestamp">
            <small>
                <span class="octicon octicon-clock"></span>
                {posted_on} by <span class="author"><b>{user_name}</b> ({title})</span>
            </small>
        <span class="controls right">
            <span class="button_margin">
                <small>
                    <a href="#" class="want_to_reply_button" {post_data_variables} ><span class="octicon octicon-comment"></span><!--Reply--></a>
                </small>
            </span>
        '''.format(text=markdown_converter.convert(self.post_text),
                   posted_on=str(self.posted_on)[:-6],
                   user_name=user.name(),
                   post_data_variables=self.addPostDataVariables(),
                   title=user.badge.name)

        if user.id == logged_user.id:
            html += '''
            <span class="button_margin">
                <small>
                    <a href="#" class="want_to_edit_button" {post_data_variables} ><span class="octicon octicon-pencil"></span><!--Edit--></a>
                </small>
            </span>
            <span class="button_margin">
                <small>
                    <a href="#" class="delete_button" {post_data_variables} ><span class="octicon octicon-x"></span><!--Delete--></a>
                </small>
            </span>'''.format(post_data_variables=self.addPostDataVariables())
        html += '</span></p>'
        return html

    # html representation of a post (highest nest)
    def HTMLString(self, logged_user):
        user = self.object_manager.createUser(id=self.user_id)

        hr = ''
        if len(self.allReplies()) != 0:
            hr = '<hr />'

        html = '''
            <div class="row">
                <div class="wall-item" data-post_id= {id}>
                    <div class="post" data-post_id= {id}>
                        {html_basic}
                        {hr}
                        <div class="replies">
        '''.format(id=str(self.id), html_basic=self.HTMLBasic(user, logged_user), hr=hr)
        for reply in self.allReplies():
            replying_user = self.object_manager.createUser(id=reply.user_id)
            html += reply.HTMLStringReply(replying_user, logged_user)
        html += '</div></div></div></div>'

        return html

    # html representation of a reply
    def HTMLStringReply(self, user, logged_user):
        hr = ''
        if len(self.allReplies()) != 0:
            hr = '<hr />'

        html = '''
            <div class="post" data-post_id= {id}>
                {html_basic}
                {hr}
                <div class="replies">
        '''.format(id=str(self.id), html_basic=self.HTMLBasic(user, logged_user), hr=hr)

        for reply in self.allReplies():
            replying_user = self.object_manager.createUser(id=reply.user_id)
            html += reply.HTMLStringReply(replying_user, logged_user)
        html += '</div></div>'

        return html
