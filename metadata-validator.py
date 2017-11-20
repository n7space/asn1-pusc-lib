import json
import shutil
import os
import glob
import sys
import subprocess

BUILD_PATH = os.path.abspath(".") + "/.dependency_check/"
ASN1SOURCES_PATH = os.path.abspath(".") + "/.dependency_check/asn1sources/"
LOG_FILE = "log.txt"

METADATA_FILENAME = "meta.json"
ASN_EXTENSION = ".asn"
ASN1_EXTENSION = ".asn1"
ACN_EXTENSION = ".acn"

SUBMODULES_KEY = "submodules"
ELEMENTS_KEY = "elements"
REQUIRES_KEY = "requires"
CONFLICTS_KEY = "conflicts"
NAME_KEY = "name"
MODULE_NAME_KEY = "module_name"
ASN1FILES_KEY = "asn1Files"
IMPORTS_KEY = "imports"
FROM_KEY = "from"

MODULE_NAME_KEY = "module_name"
METADATA_KEY = "meta_json"
METADATA_PATH_KEY = "meta_path"


ASN1SCC = "asn1.exe"
ASN1SCC_ARGS = "-ACN -c"
ASN1SCC_OUT_PATH = BUILD_PATH
CC = "gcc"
CC_ARGS = "-c -pipe -O2 -fPIC -Wall -W"
CC_OUT_PATH = BUILD_PATH
CC_SRC_PATH = BUILD_PATH
AR = "ar"
AR_ARGS = "cqs"
AR_OUT_PATH = BUILD_PATH


def getRecursiveDependency(element_lib, element):
    dependencies = []
    if ASN1FILES_KEY in element:
        for element_filename in element[ASN1FILES_KEY]:
            dependencies.append(element[METADATA_PATH_KEY] + element_filename)

            acn_filename = element[METADATA_PATH_KEY] + os.path.splitext(element_filename)[0] + ACN_EXTENSION
            if os.path.exists(acn_filename):
                dependencies.append(acn_filename)
    
    if IMPORTS_KEY in element:
        for imported in element[IMPORTS_KEY]:
            for item in element_lib:
                if ASN1FILES_KEY in item:
                    if imported[FROM_KEY] in [os.path.splitext(x)[0] for x in item[ASN1FILES_KEY]]:
                        dependencies += getRecursiveDependency(element_lib, item) 
    
    return dependencies

def logError(path, message, element, filepath):
    print("\033[1;37;49m%s: \033[1;31;49m%s: \033[0;37;49m%s" % (path, message, element))
    with open(filepath, "a+") as f:
        f.write("\n" + path + ": " + message + ": " + element)

def errorCheck(error_flag):
    if error_flag:
        print("\033[1;31;49mMetadata validation failed")
        sys.exit(1)
    else:
        print("\033[1;32;49mMetadata validation passed\033[0;37;49m")

def main():
    if os.path.isfile(BUILD_PATH + LOG_FILE):
        os.remove(BUILD_PATH + LOG_FILE)

    metadata = []
    files = glob.glob(os.path.join(os.path.abspath("."), "*/" + METADATA_FILENAME))
    for filepath in files:
        with open(filepath) as f:
            metadata.append({METADATA_KEY: json.load(f), METADATA_PATH_KEY: filepath.replace(METADATA_FILENAME, "")})
    
    element_lib = []
    for meta in metadata:
        if SUBMODULES_KEY in meta[METADATA_KEY]: 
            for submodule in meta[METADATA_KEY][SUBMODULES_KEY]:
                if ELEMENTS_KEY in submodule: 
                    for element in submodule[ELEMENTS_KEY]:
                        element[METADATA_PATH_KEY] = meta[METADATA_PATH_KEY]
                        element[MODULE_NAME_KEY] = meta[METADATA_KEY][NAME_KEY]
                        element_lib.append(element)

    error_flag = False;
    
    print("\nVerifying internal metadata dependencies")
    for element in element_lib:
        if CONFLICTS_KEY in element: 
            for conflicting in element[CONFLICTS_KEY]:
                if conflicting not in [x[NAME_KEY] for x in element_lib if x[MODULE_NAME_KEY] == element[MODULE_NAME_KEY]]:
                    logError(element[METADATA_PATH_KEY] + METADATA_FILENAME, "Could not find conflicting element", conflicting, BUILD_PATH + LOG_FILE)
                    error_flag = True

        if REQUIRES_KEY in element: 
            for required in element[REQUIRES_KEY]:
                if required not in [x[NAME_KEY] for x in element_lib if x[MODULE_NAME_KEY] == element[MODULE_NAME_KEY]]:
                    logError(element[METADATA_PATH_KEY] + METADATA_FILENAME, "Could not find required element", required, BUILD_PATH + LOG_FILE)

                    error_flag = True

        if ASN1FILES_KEY in element: 
            for element_filename in element[ASN1FILES_KEY]:
                if element_filename not in [x for x in os.listdir(element[METADATA_PATH_KEY]) if os.path.isfile(element[METADATA_PATH_KEY] + x)]:
                    logError(element[METADATA_PATH_KEY] + METADATA_FILENAME, "Could not find ASN.1 file", element_filename, BUILD_PATH + LOG_FILE)

                    error_flag = True

   
    errorCheck(error_flag)
    
    print("\nVeryfing external metadata dependencies")

    for element in element_lib:
        if IMPORTS_KEY in element: 
            for imported in element[IMPORTS_KEY]:
                if imported[FROM_KEY] not in [os.path.splitext(asn_file)[0] for item in element_lib if ASN1FILES_KEY in item for asn_file in item[ASN1FILES_KEY]]:
                    logError(element[METADATA_PATH_KEY] + METADATA_FILENAME, "Could not find module for import", imported[FROM_KEY], BUILD_PATH + LOG_FILE)
                    error_flag = True
                    
    errorCheck(error_flag)

    print("\nGenerating and building C files")

    try:
        if(os.path.isdir(BUILD_PATH)):
            shutil.rmtree(BUILD_PATH)

        os.mkdir(BUILD_PATH)
    except OSError:
        print("Error when creating directory: %s" (BUILD_PATH))
        sys.exit(1)

    for element in element_lib:
        try:
            [os.remove(x) for x in glob.glob(ASN1SCC_OUT_PATH + "*.c")]
            [os.remove(x) for x in glob.glob(ASN1SCC_OUT_PATH + "*.h")]
            [os.remove(x) for x in glob.glob(CC_OUT_PATH + "*.o")]
            [os.remove(x) for x in glob.glob(AR_OUT_PATH + "*.a")]

        except OSError:
            print("Error when removing temporary files: %s" (BUILD_PATH))
            sys.exit(1)
        
        dependencies = set(getRecursiveDependency(element_lib, element))

        if len(dependencies):
            asn1scc_command = ASN1SCC + " " +  ASN1SCC_ARGS + " " + (" ".join(dependencies)) + " -o " + ASN1SCC_OUT_PATH

            print(asn1scc_command)
            return_code =  os.system(ASN1SCC + " " +  ASN1SCC_ARGS + " " + (" ".join(dependencies)) + " -o " + ASN1SCC_OUT_PATH)
            if return_code:
                logError(element[METADATA_PATH_KEY] + METADATA_FILENAME, "Element imported in ASN.1 but not declared in metadata", element[NAME_KEY], BUILD_PATH + LOG_FILE)
                error_flag = True
            
            else:
                cfiles = glob.glob(ASN1SCC_OUT_PATH + "*.c")
                for src in cfiles:
                    compile_command = CC + " " +  CC_ARGS + " -I " + CC_SRC_PATH + " " + src + " -o " + CC_OUT_PATH + os.path.splitext(os.path.basename(src))[0] + ".o"

                    print(compile_command)
                    return_code = os.system(compile_command)
                    if return_code:
                        error_flag = True
                    
                ar_command = AR + " " + AR_ARGS + " " + AR_OUT_PATH + element[NAME_KEY].replace(" ", "_") + ".a " +  " ".join(glob.glob(CC_OUT_PATH + "*.o"))

                print(ar_command)
                return_code = os.system(ar_command)

                if return_code:
                    logError(element[METADATA_PATH_KEY] + METADATA_FILENAME, "Compilation error", element[NAME_KEY], BUILD_PATH + LOG_FILE)
                    error_flag = True

            print()
    
    errorCheck(error_flag)
    sys.exit(0)

main()
