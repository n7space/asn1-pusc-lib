TEMPLATE = lib
CONFIG += static
CONFIG -= qt

DISTFILES += \
    service-17/meta.json \
    service-17/PUS-17-1.acn \
    service-17/PUS-17-1.asn1 \
    service-17/PUS-17-2.acn \
    service-17/PUS-17-2.asn1 \
    service-17/PUS-17-3.acn \
    service-17/PUS-17-3.asn1 \
    service-17/PUS-17-4.acn \
    service-17/PUS-17-4.asn1 \
    common/ApplicationProcess.acn \
    common/ApplicationProcess.asn1 \
    common/BasicTypes.acn \
    common/BasicTypes.asn1

include(.qmake/handleAsn1AcnBuild.pri)
