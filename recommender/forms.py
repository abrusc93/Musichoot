from django import forms

class SearchForm(forms.Form):
    artist = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    from_year = forms.IntegerField(required=False)
    to_year = forms.IntegerField(required=False)

class PlaylistAddForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'size': '20', 'placeholder': 'Playlist Title'}))


class UserSearchForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))

class UserDetailsForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    playlists = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))

class FindSongForm(forms.Form):
    artist = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}), required=False)
    song_name = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}), required=False)
