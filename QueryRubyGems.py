#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3.5

import urllib.request
import json
import codecs
import sys

import logging

# Display instructions for how to use this tool.
def display_instructions():
    print("Query Ruby Gems Tool")
    print()
    print("Instructions:")
    print("Run this command-line tool to query license details of a Ruby Gem.")
    print()
    print("Usage:")
    print("{} <Ruby Gem Name> <Version (optional)>".format(sys.argv[0]))
    print()
    print("Examples:")
    print("Query the latest version of 'cucumber'")
    print("{} cucumber".format(sys.argv[0]))
    print()
    print("Query all versions of 'cucumber'")
    print("{} cucumber All".format(sys.argv[0]))
    print()
    print("Query specific version of 'cucumber'")
    print("{} cucumber 2.3.0".format(sys.argv[0]))

# Determine if arguments are sufficient
# Arguments are sufficient if at least one argument (Ruby Gem name) is specified
# Note: First argument is command line
def arguments_sufficient(args):
    if len(args) > 1:
        return True
    else:
        return False

# Parse arguments and return the gem name and gem version
def parse_arguments(arguments):

    print("******")
    print("Arguments = " + str(arguments))
    gem_name = arguments[1]
    gem_version = ""

    if len(arguments) > 2:
        gem_version = arguments[2]
    return (gem_name, gem_version)

# display license information for Ruby Gem
def display_ruby_gem_details(gem_name, ruby_gem_details):
    description = ""
    description += "Name = {}".format(gem_name)
    description += ", Version = {}".format(ruby_gem_details['number'])
    description += ", License = {}".format(ruby_gem_details['licenses'])
    print(description)

def main():

    # Parse command-line arguments
    arguments = sys.argv
    if not arguments_sufficient(arguments):
        print("Insufficient arguments!")
        display_instructions()
        return

    gem_name, gem_version = parse_arguments(arguments)

    print("Querying for gem w/name: {}".format(gem_name))
    print("Version: {}".format(gem_version))

    logging.debug("Initializing UTF-8 reader...")
    reader = codecs.getreader("utf-8")

    base_url = "https://rubygems.org/api/v1/versions/"
    queryPackage = gem_name

    complete_url = base_url + queryPackage + ".json"
    logging.debug("Querying Ruby Gems with name containing string: {}".format(queryPackage))
    logging.debug("Querying Ruby Gems web service: {}".format(complete_url))

    try:
        logging.debug("Attempting to call web service w/URL: {}".format(complete_url))
        req = urllib.request.Request(complete_url)
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        logging.error(e)
        print("Unable to connect to remote service: {}".format(e))
        print("Please check your internet connection (and Ruby Gems service URL) and try again.")
        raise("Failed to connect to remote web service.", e)

    logging.debug("Web service call succeeded. Response received")

    if not result:
        logging.warning("0 matching Ruby Gems found with name: {}.".format(gem_name))
    else:
        results_count = len(result)
        logging.info("{} versions of Ruby Gem {} found.".format(results_count, gem_name))

        if gem_version == "":
            print("Displaying license information for the latest release:")
            first_result = result[0]
            display_ruby_gem_details(gem_name, first_result)
        elif gem_version == "All":
            print("Displaying license information for all releases:")
            # Iterate over and display all Ruby Gem versions
            for each_version in result:
                display_ruby_gem_details(gem_name, each_version)
        else:
            print("Displaying license information for version: {}".format(gem_version))

            # Query list to find matching version
            filtered = filter(lambda t: t['number']==gem_version, result)

            # Convert filter object to list so that we can check row count
            filtered = list(filtered)
            if len(filtered) == 0:
                message1 = "No version {} found for Ruby Gem: '{}'".format(gem_version, gem_name)
                message2 = "Try querying with version flag 'All' to list all available versions."
                print(message1)
                print(message2)
            else:
                for next_record in filtered:
                    display_ruby_gem_details(gem_name, next_record)
        return









if __name__ == "__main__":
    main()
