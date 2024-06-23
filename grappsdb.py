from api import API
import jsons

# Dummy Classes for the jsons function
class NameD:
    pass

class DateD:
    pass

class SurnameD:
    pass

class PersonD:
    pass

class EventRefD:
    pass

class EventD:
    pass
class PlaceD:
    pass
    
class AltNameD:
    pass

class MediaD:
    pass

class FamilyD:
    pass

class WebAPI:
    def get_handle(self): return self.web_api.handle

class Person(WebAPI):
    def __init__(self, web_api):
        self.web_api = web_api

class Event(WebAPI):
    def __init__(self, web_api):
        self.web_api = web_api

class Place(WebAPI):
    def __init__(self, web_api):
        self.web_api = web_api

class Family(WebAPI):
    def __init__(self, web_api):
        self.web_api = web_api

class GrappsDB:
    def __init__(self, host, uname, pword):
        api = API( host=host, basic_auth = (uname, pword) )
        self.api = api

        self.people = self.read_people()
        self.events = self.read_events()
        self.places = self.read_places()
        self.families = self.read_families()

        # Build up dictionaries
        self.people_dict = {}
        for p in self.people:
            self.people_dict[p.get_handle()] = p
        self.events_dict = {}
        for e in self.events:
            #if e.get_handle() == 'c2dd1e77cf71eed880e':
                self.events_dict[e.get_handle()] = e
        self.places_dict = {}
        for p in self.places:
            self.places_dict[p.get_handle()] = p
        self.families_dict = {}
        for f in self.families:
            self.families_dict[f.get_handle()] = f

    def read_people(self):
        iter = self.api.iter_people()
        
        people = []
        for json in iter:
            # Read in the data as a web person
            wperson = jsons.load(json, PersonD)
            # Now, each dictionary must also be translated to a class (using jsons)
            primary_name = jsons.load(wperson.primary_name, NameD)
            primary_name.date = jsons.load(primary_name.date, DateD)
            surnames = []
            for surname in primary_name.surname_list:
                surnames.append(jsons.load(surname, SurnameD))
            primary_name.surname_list = surnames
            wperson.primary_name = primary_name
            # Event references
            event_refs = []
            for e in wperson.event_ref_list:
                event_refs.append(jsons.load(e, EventRefD))
            wperson.event_ref_list = event_refs
            
            people.append(Person(wperson)) # Make an actual person out of this and add to our list

        return people
    
    def read_events(self):
        iter = self.api.iter_events()
        
        events = []
        for json in iter:
            wevent = jsons.load(json, EventD)
            wevent.date = jsons.load(wevent.date, DateD)
            events.append(Event(wevent))
        
        # We have all the events
        return events

    def read_places(self):
        iter = self.api.iter_places()
            
        places = []
        for json in iter:
            wplace = jsons.load(json, PlaceD) # Load up the place
            
            new_alt_names = []
            alt_names = wplace.alt_names
            for alt_name in alt_names:
                alt_name = jsons.load(alt_name, AltNameD)
                alt_name.date = jsons.load(alt_name.date, DateD)
                new_alt_names.append(alt_name)
            
            new_media_list = []
            medias = wplace.media_list
            for media in medias:
                media = jsons.load(wplace.media_list[0], MediaD)
                new_media_list.append(media)
            wplace.media_list = new_media_list
            wplace.alt_names = new_alt_names
            name = jsons.load(wplace.name, AltNameD)

            name.date = jsons.load(name.date, DateD)
            wplace.name = name
            places.append(Place(wplace))

        return places

    def read_families(self):
        iter = self.api.iter_families()
        families = []
        for json in iter:
            wfamily = jsons.load(json, FamilyD)
            families.append(Family(wfamily))
        return families
        
    def get_person(self, handle):
        return self.people_dict[handle]
        
    def get_event(self, handle):
        return self.event_dict[handle]
        
    def get_place(self, handle):
        return self.place_dict[handle]

    def get_family(self, handle):
        return self.family_dict[handle]