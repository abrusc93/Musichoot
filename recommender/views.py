
from django.shortcuts import render
from django.http import Http404
from .models import *
from .forms import *
from django.views.decorators.http import require_POST, require_GET
import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django import db
from django.views.decorators.csrf import csrf_exempt

def lookup_song(id):
    try:
        song_entry = Musicdata.objects.all().filter(id=id).get()
        return song_entry
    except ObjectDoesNotExist:
        return None


def find_song(artist, song_name = None):
    query = Musicdata.objects.filter(name__contains = song_name)
    if artist is not None:
        query = query.filter(artists__contains = artist)
    return list(query.order_by('-popularity').values('id','name', 'year'))
    


def find_albums(artist, from_year = None, to_year = None):
    query = Musicdata.objects.filter(artists__contains = artist)
    if from_year is not None:
        query = query.filter(year__gte = from_year)
    if to_year is not None:
        query = query.filter(year__lte = to_year)
    db.connections.close_all()
    return list(query.order_by('-popularity').values('id','name','year'))

def find_users(username):
    query = User.objects.filter(username=username)
    db.connections.close_all()
    return list(query.values('username'))
    

def home(request):
    form2 = PlaylistAddForm()
    most_liked = Musicdata.objects.order_by('-like_count')[:4]
    playlistsload = Playlist.objects.order_by('-like_count')[:2]
    recentusers = User.objects.order_by('-last_login')[:4]
    playlists = []
    #iterate through each playlist in the list of playlist
    for playlist in playlistsload:
        #add all the songs from the selected playlist
        songs = []
        songsload = playlist.songs.all()
        for song in songsload:
            if song.likes.filter(id=request.user.id).exists():
                songs.append([song, True])
            else:
                songs.append([song, False])
        #load the specific playlist and all of that playlist songs to an array and see if current user liked the playlist
        if playlist.likes.filter(id=request.user.id).exists():
            playlists.append([playlist, songs, True])
        else:
            playlists.append([playlist, songs, False])

    answer = []
    if request.user.is_authenticated:
        for song in most_liked:
            if song.likes.filter(id=request.user.id).exists():
                answer.append([song, True])
            else:
                answer.append([song, False])
    if request.user.is_authenticated:
        userplaylists = Playlist.newmanager.filter(owner=request.user)
    else:
        userplaylists = []

    context = {
        'albums': answer,
        'form2': form2,
        'most_liked': most_liked,
        'playlists' : playlists,
        'users' : recentusers,
        'userplaylists': userplaylists
    }
    return render(request, 'home.html', context=context)


def about(request):
    return render(request, 'about/about.html')


def about_team(request):
    return render(request, 'about/team.html')


@require_POST
def searchform_post(request):
    # create a form instance and populate it with data from the request:
    form = SearchForm(request.POST)

    form2 = PlaylistAddForm()
    # check whether it's valid:
    if form.is_valid():
        # process the data in form.cleaned_data as required
        from_year = None if form.cleaned_data['from_year'] == None else int(form.cleaned_data['from_year'])
        to_year = None if form.cleaned_data['to_year'] == None else int(form.cleaned_data['to_year'])
        albums = find_albums(
                form.cleaned_data['artist'],
                from_year,
                to_year
            )
        
        # Random 3 of top 10 popular albums
        answer = albums[:10]
        random.shuffle(answer)
        answer = list(answer)[:3]
        answer2 = []
        for song_entry in answer:
            song = lookup_song(song_entry['id'])
            if song.likes.filter(id=request.user.id).exists():
                answer2.append([song, True])
            else:
                answer2.append([song, False])
        if request.user.is_authenticated:
            playlistsload = Playlist.newmanager.filter(owner=request.user)
        else:
            playlistsload = []
        db.connections.close_all()

        return render(request, 'recommender/searchform.html', {'form': form, 'form2': form2, 'albums': answer2, 'playlists' : playlistsload })
    else:
        raise Http404('Something went wrong')


@require_GET
def searchform_get(request):
    form = SearchForm()
    db.connections.close_all()
    return render(request, 'recommender/searchform.html', {'form': form})


@ login_required
@require_POST
def playlist_post(request):
    form = PlaylistAddForm(request.POST)
    if form.is_valid():
        title = None if form.cleaned_data['name'] == None else form.cleaned_data['name']
        playlist_entry = Playlist()
        playlist_entry.title = title
        playlist_entry.save()
        playlist_entry.owner.add(request.user)
        playlist_entry.save()
    #load all playlist by current user
    playlistsload = Playlist.newmanager.filter(owner=request.user)
    #create array list to pass to html
    playlists = []
    #iterate through each playlist in the list of playlist
    for playlist in playlistsload:
        #add all the songs from the selected playlist
        songs = playlist.songs.all()
        answer2  = []
        for song in songs:
            if song.likes.filter(id=request.user.id).exists():
                answer2.append([song, True])
            else:
                answer2.append([song, False])
        #load the specific playlist and all of that playlist songs to an array
        playlists.append([playlist, answer2])

    context = {
        'playlists' : playlists,
        'form' : form
    }
    db.connections.close_all()
    return render(request, 'recommender/playlist.html', context=context)

@csrf_exempt
@ login_required
@require_POST
def playlistadd_post(request, songid):
    form = PlaylistAddForm(request.POST)
    songadd = get_object_or_404(Musicdata, id=songid)
    if form.is_valid():
        title = None if form.cleaned_data['name'] == None else form.cleaned_data['name']
        playlist_entry = Playlist()
        playlist_entry.title = title
        playlist_entry.save()
        playlist_entry.owner.add(request.user)
        playlist_entry.songs.add(songadd)
        playlist_entry.save()
    #load all playlist by current user
    playlistsload = Playlist.newmanager.filter(owner=request.user)
    #create array list to pass to html
    playlists = []
    #iterate through each playlist in the list of playlist
    for playlist in playlistsload:
        #add all the songs from the selected playlist
        songs = playlist.songs.all()
        answer2  = []
        for song in songs:
            if song.likes.filter(id=request.user.id).exists():
                answer2.append([song, True])
            else:
                answer2.append([song, False])
        #load the specific playlist and all of that playlist songs to an array
        playlists.append([playlist, answer2])

    context = {
        'playlists' : playlists,
        'form' : form
    }
    db.connections.close_all()
    return render(request, 'recommender/playlist.html', context=context)


@ login_required
@require_GET
def playlist_get(request):
    form = PlaylistAddForm()
    #load all playlist by current user
    playlistsload = Playlist.newmanager.filter(owner=request.user)
    #create array list to pass to html
    playlists = []
    #iterate through each playlist in the list of playlist
    for playlist in playlistsload:
        #add all the songs from the selected playlist
        songs = playlist.songs.all()
        answer2  = []
        for song in songs:
            if song.likes.filter(id=request.user.id).exists():
                answer2.append([song, True])
            else:
                answer2.append([song, False])
        #load the specific playlist and all of that playlist songs to an array
        playlists.append([playlist, answer2])

    context = {
        'playlists' : playlists,
        'form' : form
    }
    db.connections.close_all()
    return render(request, 'recommender/playlist.html', context=context)


@ login_required
@require_GET
def playlistadd_get(request, playlistid, songid):
    form = PlaylistAddForm()
    #load playlist and song to be added
    playlistadd = get_object_or_404(Playlist, id=playlistid)
    songadd = get_object_or_404(Musicdata, id=songid)
    #add the song to the select playlist and save
    playlistadd.songs.add(songadd)
    playlistadd.save()
    #load all playlist by current user
    playlistsload = Playlist.newmanager.filter(owner=request.user)
    #create array list to pass to html
    playlists = []
    #iterate through each playlist in the list of playlist
    for playlist in playlistsload:
        #add all the songs from the selected playlist
        songs = playlist.songs.all()
        answer2  = []
        for song in songs:
            if song.likes.filter(id=request.user.id).exists():
                answer2.append([song, True])
            else:
                answer2.append([song, False])
        #load the specific playlist and all of that playlist songs to an array
        playlists.append([playlist, answer2])

    context = {
        'playlists' : playlists,
        'form' : form
    }
    db.connections.close_all()
    return render(request, 'recommender/playlist.html', context=context)

@ login_required
def playlistdeletesong(request, playlistid, songid):
    form = PlaylistAddForm()
    #load playlist and song to be deleted
    playlistdelete = get_object_or_404(Playlist, id=playlistid)
    songdelete = get_object_or_404(Musicdata, id=songid)
    #delete the song from the selected playlist
    playlistdelete.songs.remove(songdelete)
    playlistdelete.save()
    #load all playlist by current user
    playlistsload = Playlist.newmanager.filter(owner=request.user)
    #create array list to pass to html
    playlists = []
    #iterate through each playlist in the list of playlist
    for playlist in playlistsload:
        #add all the songs from the selected playlist
        songs = playlist.songs.all()
        answer2  = []
        for song in songs:
            if song.likes.filter(id=request.user.id).exists():
                answer2.append([song, True])
            else:
                answer2.append([song, False])
        #load the specific playlist and all of that playlist songs to an array
        playlists.append([playlist, answer2])

    context = {
        'playlists' : playlists,
        'form' : form
    }
    db.connections.close_all()
    return render(request, 'recommender/playlist.html', context=context)

@ login_required
def playlistdelete(request, playlistid):
    form = PlaylistAddForm()
    #delete playlist
    Playlist.objects.filter(id=playlistid).delete()
    #load all playlist by current user
    playlistsload = Playlist.newmanager.filter(owner=request.user)
    #create array list to pass to html
    playlists = []
    #iterate through each playlist in the list of playlist
    for playlist in playlistsload:
        #add all the songs from the selected playlist
        songs = playlist.songs.all()
        answer2  = []
        for song in songs:
            if song.likes.filter(id=request.user.id).exists():
                answer2.append([song, True])
            else:
                answer2.append([song, False])
        #load the specific playlist and all of that playlist songs to an array
        playlists.append([playlist, answer2])

    context = {
        'playlists' : playlists,
        'form' : form
    }
    db.connections.close_all()
    return render(request, 'recommender/playlist.html', context=context)

@ login_required
def playlistpublic(request, playlistid, public):
    form = PlaylistAddForm()
    playlist = Playlist.objects.filter(id=playlistid).get()
    if public == 'F':
        playlist.is_public = False
    else:
        playlist.is_public = True
    playlist.save()
    #load all playlist by current user
    playlistsload = Playlist.newmanager.filter(owner=request.user)
    #create array list to pass to html
    playlists = []
    #iterate through each playlist in the list of playlist
    for playlist in playlistsload:
        #add all the songs from the selected playlist
        songs = playlist.songs.all()
        answer2  = []
        for song in songs:
            if song.likes.filter(id=request.user.id).exists():
                answer2.append([song, True])
            else:
                answer2.append([song, False])
        #load the specific playlist and all of that playlist songs to an array
        playlists.append([playlist, answer2])

    context = {
        'playlists' : playlists,
        'form' : form
    }
    db.connections.close_all()
    return render(request, 'recommender/playlist.html', context=context)

@require_POST
def user_searchform_post(request):
    form = UserSearchForm(request.POST)
    
    if form.is_valid():

        userslist = find_users(form.cleaned_data['username'])

        db.connections.close_all()

        users = User.objects.all()
        return render(request, 'recommender/user_searchform.html', {'form':form, 'users':userslist, 'allusers':users})
    else:
        raise Http404('Something went wrong')

@require_GET
def user_searchform_get(request):
    form = UserSearchForm()
    db.connections.close_all()
    users = User.objects.all()
    return render(request,'recommender/user_searchform.html', {'form': form, 'allusers':users})

@require_GET
def user_info(request, username):
    form = UserDetailsForm()
    searchuser = User.objects.filter(username=username)
    searchuser = searchuser.first()
    playlistsload = Playlist.newmanager.filter(owner=searchuser)
    #create array list to pass to html
    playlists = []

    #iterate through each playlist in the list of playlist
    for playlist in playlistsload:
        #add all the songs from the selected playlist
        songs = playlist.songs.all()
        #load the specific playlist and all of that playlist songs to an array and see if current user liked the playlist
        if playlist.likes.filter(id=request.user.id).exists():
            playlists.append([playlist, songs, True])
        else:
            playlists.append([playlist, songs, False])

    context = {
        'playlists' : playlists,
        'form' : form,
        'searchuser' : searchuser
    }

    return render(request, 'recommender/user_details.html', context)

def friend_request(request):
    return render(request, 'accounts/friend_requests.html')

def showslides(request):
    return render(request, 'home.html')
  
@ login_required
def like_list(request, id, add):
    form = PlaylistAddForm()
    song = get_object_or_404(Musicdata, id=id)
    if song.likes.filter(id=request.user.id).exists() and add == 'F':
        song.likes.remove(request.user)
        song.like_count -= 1
        song.save()
    elif not song.likes.filter(id=request.user.id).exists() and add == 'T':
        song.likes.add(request.user)
        song.like_count += 1
        song.save()

    albums = Musicdata.newmanager.filter(likes=request.user)
    playlistsload = Playlist.newmanager.filter(likes=request.user)
    playlists = []
    #iterate through each playlist in the list of playlist
    for playlist in playlistsload:
        #add all the songs from the selected playlist
        songs = playlist.songs.all()
        answer2  = []
        for song in songs:
            if song.likes.filter(id=request.user.id).exists():
                answer2.append([song, True])
            else:
                answer2.append([song, False])
        #load the specific playlist and all of that playlist songs to an array
        playlists.append([playlist, answer2])
    i = 0
    answer = []
    for song in albums:
        answer.append([song,i])
        i += 1
    if request.user.is_authenticated:
        userplaylists = Playlist.newmanager.filter(owner=request.user)
    else:
        userplaylistsload = []
    return render(request,
                  'recommender/likes.html',
                  {'albums': answer, 'playlists': playlists, 'userplaylists': userplaylists, 'form2': form})

@ login_required
def playlistlike_list(request, id, add):
    playlist = get_object_or_404(Playlist, id=id)
    if playlist.likes.filter(id=request.user.id).exists() and add == 'F':
        playlist.likes.remove(request.user)
        playlist.like_count -= 1
        playlist.save()
    elif not playlist.likes.filter(id=request.user.id).exists() and add == 'T':
        playlist.likes.add(request.user)
        playlist.like_count += 1
        playlist.save()

    albums = Musicdata.newmanager.filter(likes=request.user)
    playlistsload = Playlist.newmanager.filter(likes=request.user)
    playlists = []
    #iterate through each playlist in the list of playlist
    for playlist in playlistsload:
        #add all the songs from the selected playlist
        songs = playlist.songs.all()
        answer2  = []
        for song in songs:
            if song.likes.filter(id=request.user.id).exists():
                answer2.append([song, True])
            else:
                answer2.append([song, False])
        #load the specific playlist and all of that playlist songs to an array
        playlists.append([playlist, answer2])

    i = 0
    answer = []
    for song in albums:
        answer.append([song,i])
        i += 1
    if request.user.is_authenticated:
        userplaylists = Playlist.newmanager.filter(owner=request.user)
    else:
        userplaylistsload = []
    return render(request,
                  'recommender/likes.html',
                  {'albums': answer, 'playlists': playlists, 'userplaylists': userplaylists})

@ login_required
def profilelikes(request):
    albums = Musicdata.newmanager.filter(likes=request.user)
    playlistsload = Playlist.newmanager.filter(likes=request.user)
    playlists = []
    #iterate through each playlist in the list of playlist
    for playlist in playlistsload:
        #add all the songs from the selected playlist
        songs = playlist.songs.all()
        answer2 = []
        for song in songs:
            if song.likes.filter(id=request.user.id).exists():
                answer2.append([song, True])
            else:
                answer2.append([song, False])
        #load the specific playlist and all of that playlist songs to an array
        playlists.append([playlist, answer2])
    i = 0
    answer = []
    for song in albums:
        answer.append([song,i])
        i += 1

    if request.user.is_authenticated:
        userplaylists = Playlist.newmanager.filter(owner=request.user)
    else:
        userplaylistsload = []
    return render(request, 'recommender/likes.html',
                  {'albums': answer, 'playlists': playlists, 'userplaylists': userplaylists})

@require_GET
def searchbysong_get(request):
    form = FindSongForm()
    return render(request, 'recommender/searchbysong.html', {'form': form})

@require_POST
def searchbysong_post(request):
    form2 = PlaylistAddForm()
     # create a form instance and populate it with data from the request:
    form = FindSongForm(request.POST)
    # check whether it's valid:
    if form.is_valid():
        # process the data in form.cleaned_data as required
        song_name = None if form.cleaned_data['song_name'] == None else form.cleaned_data['song_name']
        songs = find_song(
                form.cleaned_data['artist'],
                song_name
            )
        #Most populary 3 search results
        songs = songs[:3]
        answer2 = []
        for song_entry in songs:
            song = lookup_song(song_entry['id'])
            if song.likes.filter(id=request.user.id).exists():
                answer2.append([song, True])
            else:
                answer2.append([song, False])
        if request.user.is_authenticated:
            playlistsload = Playlist.newmanager.filter(owner=request.user)
        else:
            playlistsload = []
        return render(request, 'recommender/searchbysong.html', {'form': form, 'form2': form2, 'songs': answer2, 'playlists' : playlistsload })
    else:
        raise Http404('Something went wrong')


@ login_required
def playlistlikedelete_list(request, id):
    playlist = get_object_or_404(Playlist, id=id)
    if playlist.likes.filter(id=request.user.id).exists():
        playlist.likes.remove(request.user)
        playlist.like_count -= 1
        playlist.save()

    albums = Musicdata.newmanager.filter(likes=request.user)
    playlistsload = Playlist.newmanager.filter(likes=request.user)
    playlists = []
    #iterate through each playlist in the list of playlist
    for playlist in playlistsload:
        #add all the songs from the selected playlist
        songs = playlist.songs.all()
        answer2  = []
        for song in songs:
            if song.likes.filter(id=request.user.id).exists():
                answer2.append([song, True])
            else:
                answer2.append([song, False])
        #load the specific playlist and all of that playlist songs to an array
        playlists.append([playlist, answer2])

    i = 0
    answer = []
    for song in albums:
        answer.append([song,i])
        i += 1
    if request.user.is_authenticated:
        userplaylists = Playlist.newmanager.filter(owner=request.user)
    else:
        userplaylistsload = []
    return render(request,
                  'recommender/likes.html',
                  {'albums': answer, 'playlists': playlists, 'userplaylists': userplaylists})
