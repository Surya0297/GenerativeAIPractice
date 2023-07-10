



from flask import Flask,jsonify,request

app=Flask(__name__)

posts={}
post_id_generator=1

@app.route('/posts',methods=['POST'])
def createPost():
    global post_id_generator
    data=request.get_json()
    username=data.get('username')
    caption=data.get('caption')
    like=data.get('like')
    comment=data.get('comment')
    if username and caption:
        post={
            'username':username,
            'caption':caption,
            'like':like,
            'comment':comment
        }
        posts[post_id_generator]=post
        post_id_generator+=1
        return jsonify({'message':"Posted added Successfully."}),201
    return jsonify({'error':'username ans caption are required'}),400

@app.route('/posts',methods=['GET'])
def viewAllPosts():
    return jsonify(posts)

@app.route('/posts/<int:id>',methods=['DELETE'])
def deletePost(id):
    global posts
    post=posts[int(id)]
    if post is None:
        return jsonify({'error':'Post with this id Does not exists'}),400
    else:
        del posts[id]
        return jsonify({'message':"Posted deleted Successfully."})

@app.route('/posts/like/<int:id>',methods=['POST'])
def likePost(id):
    global posts
    post=posts[int(id)]
    if post is None:
        return jsonify({'error':'Post with this id Does not exists'}),400
    else:
        posts[id]['like']+=1
        return jsonify({'message':"Post liked Successfully."})


@app.route('/posts/comment/<int:id>',methods=['POST'])
def addComment(id):
    global posts
    post=posts[int(id)]
    if post is None:
        return jsonify({'error':'Post with this id Does not exists'}),400
    else:
        data=request.get_json()
        commnet=data.get('comment')
        post['comment'].append(commnet)
        return jsonify({'message':"Post Commented Successfully."})

if __name__=='__main__':
    app.run(debug=True)

