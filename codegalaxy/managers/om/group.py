import dbw
import managers.om.user
import managers.om.objectmanager
import datetime
import time

import os.path


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

    def getPicture(self):
        group_picture = "group_pictures/{}.png".format(self.id)
        path = "./codegalaxy/static/" + group_picture

        if os.path.isfile(path):
            group_picture = group_picture
        else:
            group_picture = "media/icons/group.png"
        return group_picture

    def disband(self):
        dbw.deleteGroup(self.id)

    # list of users
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

    def save(self):
        '''
        @brief save a group object
        '''
        dbw.updateGroup(self.id, self.group_name, self.group_type, self.created_on)

    def membershipPending(self, user_id):
        pending_group_memberships = dbw.getPendingGroupMemberships(user_id)

        for pending_group_membership in pending_group_memberships:
            if pending_group_membership['group_id'] == self.id:
                if pending_group_membership['user_id'] == user_id:
                    return True
        return False

    def insertMember(self, user_id, user_permissions, joined_on, status):
        '''
        @brief inserts a member in the group
        @param user_id the id of the user
        @param user_permissions the permissions of the user in this group
        @param joined_on the date the user joined on
        '''
        dbw.insertUserInGroup(self.id, user_id, user_permissions, joined_on, status)

    def deleteMember(self, user_id):
        dbw.deleteUserFromGroup(self.id, user_id)

    def getUserPermissions(self, user_id):
        permissions = dbw.getGroupUserPermissions(self.id, user_id)
        return int(permissions[0]['user_permissions'])

    def upgradeUserPermissions(self, user_id):
        # 0 = OWNER, 1 = ADMIN, 2 = USER
        dbw.updateUserPermissions(self.id, user_id, 1)

    def searchString(self):
        return str(self.group_name)

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

    def postOnWall(self, user_id, text):
        last_post_id = dbw.lastPostID()['last']
        if last_post_id is None:
            last_post_id = 0
        dbw.insertPost(self.id, user_id, last_post_id + 1, 0, text, str(time.strftime("%Y-%m-%d %H:%M:%S")))

    def deletePost(self, post_id):
        # we'll need to delete the replies aswell -> recursion
        replies_to_post = []
        # getting the replies to this post
        for reply in replies_to_post:
            self.deletePost(reply)
        dbw.deletePost(post_id)

    def editPost(self, post_id, text):
        dbw.updatePost(post_id, text)

    def allPosts(self):
        posts = []
        posts_info = dbw.getAllPostsForGroup(self.id)
        for info in posts_info:
            posts.append(Post(info['id'], info['group_id'], info['user_id'],
            info['reply'], info['reply_number'], info['post_text'],
            info['posted_on']))
        return posts

    def allPostsToHTML(self):
        html = ''
        all_posts = self.allPosts()
        original_posts = []
        for post in all_posts:
            if post.id == post.reply:
                original_posts.append(post)
        for post in original_posts:
            html += post.HTMLString(0)
            html += '<hr>'
        return html


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
        self.post_text = post_text.decode('ascii')
        self.posted_on = posted_on

    def __str__(self):
        return str(self.id) + ' \n' + str(self.group_id) + ' \n' + str(self.user_id) + ' \n' + str(self.reply) + ' \n' + str(self.reply_number) + ' \n' + self.post_text + '\n\n'

    def replyToPost(self, user_id, text):
        last_reply_number = dbw.lastReplyToPost(self.id)['last']
        dbw.insertPost(self.group_id, user_id, self.id, last_reply_number, text, str(time.strftime("%Y-%m-%d %H:%M:%S")))

    def allReplies(self):
        replies = []
        replies_info = dbw.getAllRepliesToPost(self.id)
        for info in replies_info:
            replies.append(Post(info['id'], info['group_id'], info['user_id'],
            info['reply'], info['reply_number'], info['post_text'],
            info['posted_on']))
        return replies

    def HTMLString(self, nest):
        object_manager = managers.om.objectmanager.ObjectManager()
        html = ''
        user = object_manager.createUser(id=self.user_id)
        html += '<div class="row">'
        if nest > 0:
            # filler for ident
            html += '<div class="large-' + str(nest + 2) + ' columns"></div>'
        html += '<div class="feed-item">'
        if nest == 0:
            html += '<div class="large-2 columns"><img src="/static/media/icons/rocket1.png"></div>'
        html += '<div class="large-' + str(10 - nest) + ' columns end">'
        html += '<p>' + self.post_text + '</p>'
        html += '<p class="feed-timestamp"><small><span class="octicon octicon-clock"></span>' + str(self.posted_on) + ' by ' + user.name() + '</small></p>'
        html += '<p><small></small></p>'
        html += '</div></div></div>'
        for reply in self.allReplies():
            if reply.id is not self.id:
                html += reply.HTMLString(nest + 1)
        return html
