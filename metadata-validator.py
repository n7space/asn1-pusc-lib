import json
import shutil
import os
import glob
import sys
import string

LIBRARY_PATH = os.path.abspath(".")
BUILD_PATH = os.path.join(LIBRARY_PATH, ".build", "dependency_check")
ASN1SOURCES_PATH = os.path.join(LIBRARY_PATH, ".build", "dependency_check", "asn1sources")
ERRORLOG_FILE = "errorlog.txt"

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
CC = "gcc"
CC_ARGS = "-c -pipe -O2 -fPIC -w"
AR = "ar"
AR_ARGS = "cqs"
AR_OUT_PATH = BUILD_PATH

REQUIRES_ERROR_MESSAGE = "Could not find conflicting element"
CONFLICTS_ERROR_MESSAGE = "Could not find required element"
ASN1FILES_ERROR_MESSAGE = "Could not find ASN.1 file"
IMPORTS_ERROR_MESSAGE =  "Could not find module for import"
CODE_GENERATION_ERROR_MESSAGE = "C code generation failed"
COMPILATION_ERROR_MESSAGE = "Compilation failed"
LIBRARY_CREATION_ERROR_MESSAGE = "Library creation failed"

VALIDATION_FAILED_MESSAGE = "\033[1;31;49mMetadata validation failed\033[0;37;0m"
VALIDATION_PASSED_MESSAGE = "\033[1;32;49mMetadata validation passed\033[0;37;0m"

ERROR_CODE = 1
SUCCESS_CODE = 0

def logError(element, message, details):
    path = os.path.join(element[METADATA_PATH_KEY], METADATA_FILENAME)
    #filepath = os.path.join(BUILD_PATH, ERRORLOG_FILE)
    print("\033[1;37;49m%s: \033[1;31;49m%s: \033[0;37;49m%s\033[0;37;0m" % (path, message, details))
    #with open(filepath, "a+") as f:
    #    f.write("path" + ": " + message + ": " + details)


def getRecursiveDependency(element, element_lib):
    dependencies = []
    for element_filename in element.get(ASN1FILES_KEY, []):
        dependencies.append(element[METADATA_PATH_KEY] + element_filename)

        acn_filename = element[METADATA_PATH_KEY] + os.path.splitext(element_filename)[0] + ACN_EXTENSION
        if os.path.exists(acn_filename):
            dependencies.append(acn_filename)
    
    for imported in element.get(IMPORTS_KEY, []):
        for item in element_lib:
            if imported[FROM_KEY] in [os.path.splitext(x)[0] for x in item.get(ASN1FILES_KEY, [])]:
                dependencies += getRecursiveDependency(item, element_lib) 
    
    return dependencies


def makeValidFilename(filename):
    valid_characters = "_-.() " + string.ascii_letters + string.digits
    return "".join(c for c in filename.replace(" ", "-") if c in valid_characters)


def getModuleElementNames(module_name, element_lib):
    return [element[NAME_KEY] for element in element_lib if module_name == element[MODULE_NAME_KEY]]


def getAsn1Modules(element_lib):
    return [os.path.splitext(asn_file)[0] for element in element_lib if ASN1FILES_KEY in element for asn_file in element[ASN1FILES_KEY]]


def checkRequiresValid(element, element_lib):
    return not [logError(element, REQUIRES_ERROR_MESSAGE, required) \
                for required in element.get(REQUIRES_KEY, []) \
                if required not in getModuleElementNames(element[MODULE_NAME_KEY], element_lib)]


def checkConflictsValid(element, element_lib):
    return not [logError(element, CONFLICTS_ERROR_MESSAGE, conflicting) \
                for conflicting in element.get(CONFLICTS_KEY, []) \
                if conflicting not in getModuleElementNames(element[MODULE_NAME_KEY], element_lib)]


def checkAsn1FilesValid(element):
    return not [logError(element, ASN1FILES_ERROR_MESSAGE, asn1file) \
                for asn1file in element.get(ASN1FILES_KEY, []) \
                if asn1file not in os.listdir(element[METADATA_PATH_KEY])]


def checkImportsValid(element, asn1_modules):
    return not [logError(element, IMPORTS_ERROR_MESSAGE, imported[FROM_KEY]) \
                for imported in element.get(IMPORTS_KEY, []) if imported[FROM_KEY] not in asn1_modules]  


def checkInternalDependenciesValid(element_lib):
    return all(checkRequiresValid(element, element_lib) and checkConflictsValid(element, element_lib) and checkAsn1FilesValid(element) \
               for element in element_lib)


def checkExternalDependenciesValid(element_lib):
    asn1_modules = getAsn1Modules(element_lib)
    return all(checkImportsValid(element, asn1_modules) for element in element_lib)


def checkCCodeGenerationValid(element, files, path):
    asn1scc_command = ASN1SCC + " " +  ASN1SCC_ARGS + " " + (" ".join(files)) + " -o " + path
    #print(asn1scc_command)

    if os.system(asn1scc_command) != 0:
        logError(element, CODE_GENERATION_ERROR_MESSAGE, element[NAME_KEY])
        return False
    else:
        return True 


def compileFile(src, path):
    cc_command = CC + " " +  CC_ARGS + " -I " + path + " " + src + " -o " + os.path.join(path, os.path.splitext((src))[0]) +  ".o"
    #print(cc_command)
    return os.system(cc_command)


def checkCompilationValid(element, path):
    return not [logError(element, COMPILATION_ERROR_MESSAGE, element[NAME_KEY]) \
                for src in glob.glob(os.path.join(path, "*.c")) if compileFile(src, path) != 0]


def checkLibraryCreationValid(element, path):
    ar_command = AR + " " + AR_ARGS + " " + os.path.join(path, "lib.a")  +  " ".join(glob.glob(os.path.join(path + "*.o")))
    #print(ar_command)

    if os.system(ar_command) != 0:
        logError(element, CODE_GENERATION_ERROR_MESSAGE, element[NAME_KEY])
        return False
    else:
        return True


def checkElementCompilationValid(element, element_lib, build_path):
    dependencies = set(getRecursiveDependency(element, element_lib))
    path = os.path.join(build_path, makeValidFilename(element[NAME_KEY]))
    print (path)
    os.makedirs(path)
    if not dependencies: return True
    if not checkCCodeGenerationValid(element, dependencies, path): return False
    if not checkCompilationValid(element, path): return False
    if not checkLibraryCreationValid(element, path): return False
    return True

def checkCodeValid(element_lib, build_path):
    return all(checkElementCompilationValid(element, element_lib, build_path) for element in element_lib)


def loadLibrary(path):
    metadata = []
    files = glob.glob(os.path.join(path, "*/" + METADATA_FILENAME))
    for filepath in files:
        with open(filepath) as f:
            metadata.append({METADATA_KEY: json.load(f), METADATA_PATH_KEY: filepath.replace(METADATA_FILENAME, "")})
    
    element_lib = []
    for meta in metadata:
        for submodule in meta[METADATA_KEY].get(SUBMODULES_KEY, []):
            for element in submodule.get(ELEMENTS_KEY, []):
                element[METADATA_PATH_KEY] = meta[METADATA_PATH_KEY]
                element[MODULE_NAME_KEY] = meta[METADATA_KEY][NAME_KEY]
                element_lib.append(element)

    return element_lib


def validateMetadata(library_path=LIBRARY_PATH, build_path=BUILD_PATH):
    try:
        if(os.path.isdir(build_path)):
            shutil.rmtree(build_path)

        os.makedirs(build_path)
    except OSError:
        print("Error when creating directory: %s" % (build_path))
        return ERROR_CODE
    
    element_lib = loadLibrary(library_path)

    print("\nVerifying internal metadata dependencies")
    if checkInternalDependenciesValid(element_lib):
        print(VALIDATION_PASSED_MESSAGE)
    else:
        print(VALIDATION_FAILED_MESSAGE)
        return ERROR_CODE

    print("\nVeryfing external metadata dependencies")
    if checkExternalDependenciesValid(element_lib):
        print(VALIDATION_PASSED_MESSAGE)
    else:
        print(VALIDATION_FAILED_MESSAGE)
        return ERROR_CODE

    print("\nGenerating and building C files")
    if checkCodeValid(element_lib, build_path):
        print(VALIDATION_PASSED_MESSAGE)
    else:
        print(VALIDATION_FAILED_MESSAGE)
        return ERROR_CODE

    return SUCCESS_CODE

if __name__ == "__main__":
    sys.exit(validateMetadata())
