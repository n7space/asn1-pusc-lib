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
    ccsds/TC-Payload.asn1 \
    service-01/Request.acn \
    service-01/Request.asn1 \
    service-02/meta.json \
    service-02/PUS-2-1-DistributeOnOffDeviceCommands.acn \
    service-02/PUS-2-1-DistributeOnOffDeviceCommands.asn1 \
    service-02/PUS-2-2-DistributeRegisterLoadCommands.acn \
    service-02/PUS-2-2-DistributeRegisterLoadCommands.asn1 \
    service-02/PUS-2-4-DistributeCpduCommands.acn \
    service-02/PUS-2-4-DistributeCpduCommands.asn1 \
    service-02/PUS-2-5-DistributeRegisterDumpCommands.acn \
    service-02/PUS-2-5-DistributeRegisterDumpCommands.asn1 \
    service-02/PUS-2-6-RegisterDumpReport.acn \
    service-02/PUS-2-6-RegisterDumpReport.asn1 \
    service-02/Registers.acn \
    service-02/Registers.asn1 \
    service-02/PUS-2-7-DistributePhysicalDeviceCommands.acn \
    service-02/PUS-2-7-DistributePhysicalDeviceCommands.asn1 \
    service-02/PhysicalDevice.acn \
    service-02/PhysicalDevice.asn1 \
    service-02/PUS-2-8-AcquireDataFromPhysicalDevices.acn \
    service-02/PUS-2-8-AcquireDataFromPhysicalDevices.asn1 \
    service-02/Transaction.acn \
    service-02/Transaction.asn1 \
    service-02/PUS-2-9-PhysicalDeviceDataReport.acn \
    service-02/PUS-2-9-PhysicalDeviceDataReport.asn1 \
    service-02/PUS-2-10-DistrubuteLogicalDeviceCommands.acn \
    service-02/PUS-2-10-DistrubuteLogicalDeviceCommands.asn1 \
    service-02/LogicalDevice.acn \
    service-02/LogicalDevice.asn1 \
    service-02/PUS-2-11-AcquireDataFromLogicalDevices.acn \
    service-02/PUS-2-11-AcquireDataFromLogicalDevices.asn1 \
    service-02/PUS-2-12-LogicalDeviceDataReport.acn \
    service-02/PUS-2-12-LogicalDeviceDataReport.asn1


include(.qmake/handleAsn1AcnBuild.pri)
