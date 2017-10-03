"""
This module should be used to test the parameter and return types of your
functions. Before submitting your assignment, run this type-checker. This
typechecker expects to find files twitterverse_functions.py, small_data.txt, 
and typecheck_query.txt in the same folder.

If errors occur when you run this typechecker, fix them before you submit
your assignment.

If no errors occur when you run this typechecker, then the type checks passed.
This means that the function parameters and return types match the assignment
specification, but it does not mean that your code works correctly in all
situations. Be sure to test your code thoroughly before submitting.
"""

import builtins

# Check for use of functions print, input and open.

our_print = print
our_input = input
our_open = open

def disable_print(*args):
    raise Exception("You must not call built-in function print!")

def disable_input(*args):
    raise Exception("You must not call built-in function input!")

def disable_open(*args):
    raise Exception("You must not call built-in function open!")

builtins.print = disable_print
builtins.input = disable_input
builtins.open = disable_open

import twitterverse_functions

# typecheck the twitterverse_functions.py functions

# Type check twitterverse_functions.process_data
open_data_file = our_open('small_data.txt')
result = twitterverse_functions.process_data(open_data_file)
open_data_file.close()
assert isinstance(result, dict), \
    '''process_data should return a dict, but returned {0}''' \
    .format(type(result))
for item in result:
    assert isinstance(item, str), \
        'process_data should return a dict with str keys, ' \
        'but returned a dict with {0} keys'\
        .format(type(item))
    assert isinstance(result[item], dict), \
           'process_data should return a dict with dict values, but returned ' \
           'a dict with {0} values'\
           .format(type(result[item]))
    for key in result[item]:
        assert isinstance(key, str), \
                'process_data should return an inner dict with str keys, ' \
                'but returned an inner dict with {0} keys'\
                .format(type(key))   
        assert isinstance(result[item][key], str) or \
               isinstance(result[item][key], list), \
                'process_data should return an inner dict with str or list '\
                'values, but returned an inner dict with {0} values'\
                .format(type(item))        
   
   
# Type check twitterverse_functions.process_query
open_query_file = our_open('typecheck_query.txt') 
result = twitterverse_functions.process_query(open_query_file)
open_query_file.close()
assert isinstance(result, dict), \
    '''process_query should return a dict, but returned {0}''' \
    .format(type(result))

# Query dictionary
assert 'search' in result, '''key 'search' missing from query dictionary'''
assert 'filter' in result, '''key 'filter' missing from query dictionary'''
assert 'present' in result, '''key 'present' missing from query dictionary'''
assert len(result) == 3, '''query dictionary has incorrect length'''

# Search specification
assert len(result['search']) == 2, \
       '''search spec dictionary has incorrect length'''
assert 'username' in result['search'], \
       '''key 'username' missing from search specification dictionary'''
assert isinstance(result['search']['username'], str), \
       "key 'username' should have value of type str, " \
       "but has value of type {0}"\
       .format(type(result['search']['username']))       
assert 'operations' in result['search'], \
       '''key 'operations' missing from search specification dictionary'''
assert isinstance(result['search']['operations'], list), \
       "key 'operations' should have value of type list, " \
       "but has value of type {0}"\
       .format(type(result['search']['operations']))

# Filter specification
assert len(result['filter']) == 4, \
       '''filter spec dictionary has incorrect length'''
for item in result['filter']:
    assert item in ['following', 'follower', 'name-includes', \
                    'location-includes'], \
        '''invalid key {0} in filter specification dictionary'''\
        .format(item)   
    assert isinstance(result['filter'][item], str), \
        'values in filter specification dictionary should have type str, ' \
        'but has type {0}'\
        .format(type(result['filter'][item]))
    
# Presentation specification
assert len(result['present']) == 2, \
       '''present spec dictionary has incorrect length'''
assert 'sort-by' in result['present'], \
       '''key 'sort-by' missing from present specification dictionary'''
assert isinstance(result['present']['sort-by'], str), \
       "key 'sort-by' should have value of type str, " \
       "but has value of type {0}"\
       .format(type(result['present']['sort-by']))  
assert 'format' in result['present'], \
       '''key 'format' missing from present specification dictionary'''
assert isinstance(result['present']['format'], str), \
       "key 'format' should have value of type str, " \
       "but has value of type {0}"\
       .format(type(result['present']['format']))  


# Type check twitterverse_functions.get_search_results
twitter_data = {'tomCruise': {'following': ['katieH'], 'name': 'Tom Cruise', 
                              'bio': 'Official TomCruise.com crew tweets. ' + \
                              'We love you guys!\nVisit us at Facebook!', 
                              'web': 'http://www.tomcruise.com', 
                              'location': 'Los Angeles, CA'}, 
                'katieH': {'following': [], 'name': 'Katie Holmes', 
                           'bio': '', 'web': 'www.tomkat.com', 'location': ''}}
search_spec = {'operations': ['following'], 'username': 'tomCruise'}
result = twitterverse_functions.get_search_results(twitter_data, search_spec)
assert isinstance(result, list), \
    '''get_search_results should return a list, but returned {0}''' \
    .format(type(result))
for item in result:
    assert isinstance(item, str), \
        'get_search_results should return a list of str, ' \
        'but returned a list of {0}'\
        .format(type(item))


# Type check twitterverse_functions.get_filter_results
twitter_data = {'tomCruise': {'following': ['katieH'], 'name': 'Tom Cruise', 
                              'bio': 'Official TomCruise.com crew tweets. ' + \
                              'We love you guys!\nVisit us at Facebook!', 
                              'web': 'http://www.tomcruise.com', 
                              'location': 'Los Angeles, CA'}, 
                'katieH': {'following': [], 'name': 'Katie Holmes', 
                           'bio': '', 'web': 'www.tomkat.com', 'location': ''}}
filter_spec = {}
result = twitterverse_functions.get_filter_results(twitter_data, ['katieH'], \
                                                   filter_spec)
assert isinstance(result, list), \
    '''get_filter_results should return a list, but returned {0}''' \
    .format(type(result))
for item in result:
    assert isinstance(item, str), \
        'get_filter_results should return a list of str, '\
        'but returned a list of {0}'\
        .format(type(item))


# Type check twitterverse_functions.get_present_string with long format
twitter_data = {'tomCruise': {'following': ['katieH'], 'name': 'Tom Cruise', 
                              'bio': 'Official TomCruise.com crew tweets. ' + \
                              'We love you guys!\nVisit us at Facebook!', 
                              'web': 'http://www.tomcruise.com', 
                              'location': 'Los Angeles, CA'}, 
                'katieH': {'following': [], 'name': 'Katie Holmes', 
                           'bio': '', 'web': 'www.tomkat.com', 'location': ''}}
present_spec = {'sort-by': 'username', 'format': 'long'}
result = twitterverse_functions.get_present_string(twitter_data, \
                                                   ['katieH', 'tomCruise'], \
                                                   present_spec)
assert isinstance(result, str), \
    '''get_present_string should return a str, but returned {0}''' \
    .format(type(result))
long_result = """----------
katieH
name: Katie Holmes
location: 
website: www.tomkat.com
bio:

following: []
----------
tomCruise
name: Tom Cruise
location: Los Angeles, CA
website: http://www.tomcruise.com
bio:
Official TomCruise.com crew tweets. We love you guys!
Visit us at Facebook!
following: ['katieH']
----------
"""
assert result == long_result, \
       '''incorrect formatting of presentation string, expected {0}\n \
       got {1}\n'''.format(long_result, result)


# Type check twitterverse_functions.get_present_string with short format
twitter_data = {'tomCruise': {'following': ['katieH'], 'name': 'Tom Cruise', 
                              'bio': 'Official TomCruise.com crew tweets. ' + \
                              'We love you guys!\nVisit us at Facebook!', 
                              'web': 'http://www.tomcruise.com', 
                              'location': 'Los Angeles, CA'}, 
                'katieH': {'following': [], 'name': 'Katie Holmes', 
                           'bio': '', 'web': 'www.tomkat.com', 'location': ''}}

present_spec = {'sort-by': 'username', 'format': 'short'}
result = twitterverse_functions.get_present_string(twitter_data, ['katieH'], \
                                                   present_spec)
assert isinstance(result, str), \
    '''get_present_string should return a str, but returned {0}''' \
    .format(type(result))
short_result = "['katieH']"
assert result == short_result, \
       '''incorrect formatting of presentation string, expected {0}\n \
       got {1}\n'''.format(short_result, result)



# Type check and simple test of twitterverse_functions.all_followers
twitter_data = {'a':{'name':'', 'location':'', 'web':'', \
                     'bio':'', 'following':['c']}, \
                'b':{'name':'', 'location':'', 'web':'', \
                     'bio':'', 'following':['c']}, \
                'c':{'name':'', 'location':'', 'web':'', \
                     'bio':'', 'following':[]}}
result = twitterverse_functions.all_followers(twitter_data, 'c')
assert isinstance(result, list), \
       '''all_followers should return a list, but returned {0}'''.\
       format(type(result))
assert 'a' in result and 'b' in result and len(result) == 2, \
       '''all_followers should return ['a', 'b'] but returned {0}'''\
       .format(result)

our_print("""

Yippee! The type checker program completed without error.

This means that the functions in twitterverse_functions.py:
- are named correctly,
- take the correct number of arguments, and
- return the correct types

This does NOT mean that the functions are correct!

Be sure to thoroughly test your functions yourself before submitting.""")

# Restore functions.
builtins.print = our_print
builtins.input = our_input
builtins.open = our_open
