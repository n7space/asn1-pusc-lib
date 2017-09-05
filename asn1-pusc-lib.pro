TEMPLATE = lib
CONFIG += static
CONFIG -= qt

DISTFILES += \
    ccsds/PacketTypes.acn \
    ccsds/PacketTypes.asn1 \
    ccsds/TC-Packet.acn \
    ccsds/TC-Packet.asn1 \
    ccsds/TM-Packet.acn \
    ccsds/TM-Packet.asn1 \
    common/ApplicationProcess.acn \
    common/ApplicationProcess.asn1 \
    common/BasicTypes.acn \
    common/BasicTypes.asn1 \
    common/ExecutionStep.acn \
    common/ExecutionStep.asn1 \
    common/meta.json \
    service-01/ErrorCodes.acn \
    service-01/ErrorCodes.asn1 \
    service-01/meta.json \
    service-01/PUS-1-10.acn \
    service-01/PUS-1-10.asn1 \
    service-01/PUS-1-1.acn \
    service-01/PUS-1-1.asn1 \
    service-01/PUS-1-2.acn \
    service-01/PUS-1-2.asn1 \
    service-01/PUS-1-3.acn \
    service-01/PUS-1-3.asn1 \
    service-01/PUS-1-4.acn \
    service-01/PUS-1-4.asn1 \
    service-01/PUS-1-5.acn \
    service-01/PUS-1-5.asn1 \
    service-01/PUS-1-6.acn \
    service-01/PUS-1-6.asn1 \
    service-01/PUS-1-7.acn \
    service-01/PUS-1-7.asn1 \
    service-01/PUS-1-8.acn \
    service-01/PUS-1-8.asn1 \
    service-01/Request-ID.acn \
    service-01/Request-ID.asn1 \
    service-09/meta.json \ 
    service-17/meta.json \
    service-17/PUS-17-1.acn \
    service-17/PUS-17-1.asn1 \
    service-17/PUS-17-2.acn \
    service-17/PUS-17-2.asn1 \
    service-17/PUS-17-3.acn \
    service-17/PUS-17-3.asn1 \
    service-17/PUS-17-4.acn \
    service-17/PUS-17-4.asn1 \
    ccsds/meta.json \
    ccsds/ApplicationProcessUser.acn \
    ccsds/ApplicationProcessUser.asn1 \
    ccsds/TM-Payload.asn1 \
    ccsds/TM-Payload.acn \
    ccsds/TC-Payload.acn \
    ccsds/TC-Payload.asn1


include(.qmake/handleAsn1AcnBuild.pri)
