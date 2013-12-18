import sys,os
import xml.etree.ElementTree as ET
import traceback

__all__ = ['GenCanIf']

__Header = \
"""/*
* Configuration of module: PduR
*
* Created by:   parai          
* Copyright:    (C)parai@foxmail.com  
*
* Configured for (MCU):    MinGW ...
*
* Module vendor:           ArcCore
* Generator version:       2.0.34
*
* Generated by easySAR Studio (https://github.com/parai/OpenSAR)
*/
"""

__dir = '.'
__root = None

def tInt(strnum):
    if(strnum.find('0x') or strnum.find('0X')):
        return int(strnum,16)
    else:
        return int(strnum,10)
    
def GenPduR(wfxml):
    global __dir,__root
    __root = ET.parse(wfxml).getroot();
    __dir = os.path.dirname(wfxml)
    GenH()
    GenC()
    
def GAGet(what,which):
    # what must be a pdu = [ Name, Id, Bus]
    if(which == 'name'):
        return what[0]
    elif(which == 'id'):
        return hex(tInt(what[1]))
    elif(which == 'bus'):
        return what[2]

def GLGet(what):
    """ Gen Get List
        Get A Special List []
    """
    global __root
    import re
    # (Type=RX/TX ) (Name) (Id)
    reMsg = re.compile(r'(\w+)\s*=\s*(\w+)\s*\(\s*(\w+)\s*\)')
    rlist =[]
    if(what == 'TxPdu'):
        for Signal in __root.find('SignalList'):
            msg = Signal.attrib['msg']
            try:
                msg = reMsg.search(msg).groups()
                if(msg[0] == 'TX'):
                   flag = False
                   for pdu in rlist:
                       # If has same Id and Bus
                       if(msg[2] == pdu[1] and Signal.attrib['bus'] == pdu[2]):
                           if(msg[1]) != pdu[0]:
                               raise Exception('Name must be the same if the message has the same Id on the same Bus.')
                           flag = True
                   if(False == flag):
                       pdu = []
                       pdu.append(msg[1])
                       pdu.append(msg[2])
                       pdu.append(Signal.attrib['bus'])
                       rlist.append(pdu)
            except:
                print traceback.format_exc()
                print 'PduR: Error Message Configured for %s'%(Signal.attrib['name'])
    elif(what == 'RxPdu'):
        for Signal in __root.find('SignalList'):
            msg = Signal.attrib['msg']
            try:
                msg = reMsg.search(msg).groups()
                if(msg[0] == 'RX'):
                   flag = False
                   for pdu in rlist:
                       if(msg[2] == pdu[1] and Signal.attrib['bus'] == pdu[2]):
                           if(msg[1]) != pdu[0]:
                               raise Exception('Name must be the same if the message has the same Id on the same Bus.')
                           flag = True
                   if(False == flag):
                       pdu = []
                       pdu.append(msg[1])
                       pdu.append(msg[2])
                       pdu.append(Signal.attrib['bus'])
                       rlist.append(pdu)
            except:
                print traceback.format_exc()
                print 'PduR: Error Message Configured for %s'%(Signal.attrib['name'])
    return rlist
def GenH():
    global __dir
    # =========================  PduR_Cfg.h ==================
    fp = open('%s/PduR_Cfg.h'%(__dir),'w')
    fp.write(__Header)
    fp.write("""
#if !(((PDUR_SW_MAJOR_VERSION == 2) && (PDUR_SW_MINOR_VERSION == 0)) )
#error PduR: Configuration file expected BSW module version to be 2.0.*
#endif

#ifndef PDUR_CFG_H_
#define PDUR_CFG_H_

// Module support
#define PDUR_CANIF_SUPPORT STD_ON
#define PDUR_CANTP_SUPPORT STD_ON
#define PDUR_FRIF_SUPPORT STD_OFF  /* Not supported */
#define PDUR_FRTP_SUPPORT STD_OFF  /* Not supported */
#define PDUR_LINIF_SUPPORT STD_OFF
#define PDUR_LINTP_SUPPORT STD_OFF  /* Not supported */
#define PDUR_COM_SUPPORT STD_ON
#define PDUR_DCM_SUPPORT STD_ON
#define PDUR_IPDUM_SUPPORT STD_OFF  /* Not supported */
#define PDUR_J1939TP_SUPPORT STD_OFF
#define PDUR_SOAD_SUPPORT STD_OFF  /* Not supported */

#if defined(USE_DET)
#define PDUR_DEV_ERROR_DETECT STD_ON
#else
#define PDUR_DEV_ERROR_DETECT STD_OFF
#endif

#define PDUR_VERSION_INFO_API        STD_ON

// Zero cost operation mode
#define PDUR_ZERO_COST_OPERATION STD_OFF
#define PDUR_SINGLE_IF CAN_IF
#define PDUR_SINGLE_TP CAN_TP
// Gateway operation
#define PDUR_GATEWAY_OPERATION                STD_OFF
#define PDUR_MEMORY_SIZE                    10 /* Not used */
#define PDUR_SB_TX_BUFFER_SUPPORT            STD_OFF
#define PDUR_FIFO_TX_BUFFER_SUPPORT            STD_OFF

/* The maximum numbers of Tx buffers. */
#define PDUR_MAX_TX_BUFFER_NUMBER            10 /* Not used */
#define PDUR_N_TP_ROUTES_WITH_BUFFER        0 //"not understand by parai"
#define PDUR_N_TP_BUFFERS                    2

// Multicast,not understand by parai
#define PDUR_MULTICAST_TOIF_SUPPORT            STD_ON
#define PDUR_MULTICAST_FROMIF_SUPPORT        STD_ON
#define PDUR_MULTICAST_TOTP_SUPPORT            STD_ON
#define PDUR_MULTICAST_FROMTP_SUPPORT        STD_ON

// Minimum routing,not understand by parai
/* Minimum routing not supported.
#define PDUR_MINIMUM_ROUTING_UP_MODULE        COM
#define PDUR_MINIMUM_ROUTING_LO_MODULE        CAN_IF
#define PDUR_MINIMUM_ROUTING_UP_RXPDUID        ((PduIdType)100)
#define PDUR_MINIMUM_ROUTING_LO_RXPDUID     ((PduIdType)255)
#define PDUR_MINIMUM_ROUTING_UP_TXPDUID     ((PduIdType)255)
#define PDUR_MINIMUM_ROUTING_LO_TXPDUID     ((PduIdType)255)
*/

#if(PDUR_ZERO_COST_OPERATION == STD_ON)
// Zero cost operation support active.
#if PDUR_CANIF_SUPPORT == STD_ON
#define PduR_CanIfRxIndication Com_RxIndication
#define PduR_CanIfTxConfirmation Com_TxConfirmation
#else
#define PduR_CanIfRxIndication(CanRxPduId,PduInfoPtr)
#define PduR_CanIfTxConfirmation(CanTxPduId)
#endif

#if PDUR_CANTP_SUPPORT == STD_ON
#define PduR_CanTpProvideRxBuffer Dcm_ProvideRxBuffer
#define PduR_CanTpRxIndication Dcm_RxIndication
#define PduR_CanTpProvideTxBuffer Dcm_ProvideTxBuffer
#define PduR_CanTpTxConfirmation Dcm_TxConfirmation
#else
#define PduR_CanTpProvideRxBuffer(id,length,PduInfoPtr)
#define PduR_CanTpRxIndication(CanTpRxPduId,Result)
#define PduR_CanTpProvideTxBuffer(CanTpTxId,PduinfoPtr,Length)
#define PduR_CanTpTxConfirmation(CanTpTxPduId,Result)
#endif

#if PDUR_LINIF_SUPPORT == STD_ON 
#define PduR_LinIfRxIndication Com_RxIndication
#define PduR_LinIfTxConfirmation Com_TxConfirmation
#define PduR_LinIfTriggerTransmit Com_TriggerTransmit
#else
#define PduR_LinIfRxIndication(LinRxPduId,PduInfoPtr)
#define PduR_LinIfTxConfirmation(LinTxPduId)
#define PduR_LinIfTriggerTransmit(LinTxPduId,PduInfoPtr)
#endif

#if PDUR_SOAD_SUPPORT == STD_ON
#define PduR_SoAdTpProvideRxBuffer Dcm_ProvideRxBuffer
#define PduR_SoAdTpRxIndication Dcm_RxIndication
#define PduR_SoAdTpProvideTxBuffer Dcm_ProvideTxBuffer
#define PduR_SoAdTpTxConfirmation Dcm_TxConfirmation
#else
#define PduR_SoAdProvideRxBuffer()
#define PduR_SoAdRxIndication()
#define PduR_SoAdProvideTxBuffer()
#define PduR_SoAdTxConfirmation()
#endif

#if PDUR_COM_SUPPORT == STD_ON
#define PduR_ComTransmit CanIf_Transmit
#else
#define PduR_ComTransmit(CanTxPduId,PduInfoPtr)    (E_OK)
#endif

#if PDUR_DCM_SUPPORT == STD_ON
#define PduR_DcmTransmit CanTp_Transmit
#else
#define PduR_DcmTransmit(CanTpTxSduId,CanTpTxInfoPtr)    (E_OK)
#endif
#endif  /* PDUR_ZERO_COST_OPERATION */

#endif /* PDUR_CFG_H_ */    
    """)
    fp.close()
    
    # =========================  PduR_Cfg.h ==================
    fp = open('%s/PduR_PbCfg.h'%(__dir),'w')
    fp.write(__Header)
    cstr = '// ---- Gen Helper ----\n'
    cstr += '#define GenPduRId(id) (id+4)\n'
    id = 0
    for pdu in GLGet('RxPdu'):
        cstr += '#define PDUR_%s_RX GenPduRId(%s)\n'%(GAGet(pdu,'name'),id)
        id += 1
    for pdu in GLGet('TxPdu'):
        cstr += '#define PDUR_%s_TX GenPduRId(%s)\n'%(GAGet(pdu,'name'),id)
        id += 1
    fp.write("""
#ifndef PDUR_PB_CFG_H_H
#define PDUR_PB_CFG_H_H
#if !(((PDUR_SW_MAJOR_VERSION == 2) && (PDUR_SW_MINOR_VERSION == 0)) )
#error PduR: Configuration file expected BSW module version to be 2.0.*
#endif

#include "Dcm.h"
#include "Com.h"
#include "CanIf.h"
#include "CanTp.h"

extern const PduR_PBConfigType PduR_Config;
//  PduR Polite Defines.
#define PDUR_DIAG_P2P_REQ        0
#define PDUR_DIAG_P2P_ACK        1
#define PDUR_DIAG_P2A_REQ        2
#define PDUR_DIAG_P2A_ACK        3

%s

#endif /* PDUR_PB_CFG_H_H */\n\n"""%(cstr))
    fp.close()
    
def GenC():   
    global __dir
    fp = open('%s/PduR_Cfg.c'%(__dir),'w')
    fp.write(__Header)
    cstr = ''
    for pdu in GLGet('RxPdu'):
        cstr += """
    { // %s
        .DataProvision =  PDUR_NO_PROVISION,
        .DestPduId =  COM_%s_RX,
        .TxBufferRef =  NULL,
        .DestModule =  ARC_PDUR_COM
    },\n"""%(GAGet(pdu,'name'),GAGet(pdu,'name'))
    for pdu in GLGet('TxPdu'):
        cstr += """
    { // %s
        .DataProvision =  PDUR_NO_PROVISION,
        .DestPduId =  CANIF_%s_TX,
        .TxBufferRef =  NULL,
        .DestModule =  ARC_PDUR_CANIF
    },\n"""%(GAGet(pdu,'name'),GAGet(pdu,'name'))
    fp.write("""

#include "PduR.h"

#if PDUR_CANIF_SUPPORT == STD_ON
#include "CanIf.h"
#endif
#if PDUR_CANTP_SUPPORT == STD_ON
#include "CanTp.h"
#endif
#if PDUR_LINIF_SUPPORT == STD_ON
#include "LinIf.h"
#endif
#if PDUR_COM_SUPPORT == STD_ON
#include "Com.h"
#endif
#if PDUR_DCM_SUPPORT == STD_ON
#include "Dcm.h"
#endif
#if PDUR_J1939TP_SUPPORT == STD_ON
#include "J1939Tp.h"
#endif
#if(PDUR_ZERO_COST_OPERATION == STD_OFF)
const PduRDestPdu_type PduR_PduRDestination[] = {

    { // DIAG_P2P_REQ
        .DataProvision =  PDUR_NO_PROVISION,
        .DestPduId =  DCM_DIAG_P2P_REQ,
        .TxBufferRef =  NULL,
        .DestModule =  ARC_PDUR_DCM
    },
    { // DIAG_P2P_ACK
        .DataProvision =  PDUR_NO_PROVISION,
        .DestPduId =  CANTP_DIAG_P2P_ACK,
        .TxBufferRef =  NULL,
        .DestModule =  ARC_PDUR_CANTP
    },
    { // DIAG_P2A_REQ
        .DataProvision =  PDUR_NO_PROVISION,
        .DestPduId =  DCM_DIAG_P2A_REQ,
        .TxBufferRef =  NULL,
        .DestModule =  ARC_PDUR_DCM
    },
    { // DIAG_P2A_ACK
        .DataProvision =  PDUR_NO_PROVISION,
        .DestPduId =  CANTP_DIAG_P2A_ACK,
        .TxBufferRef =  NULL,
        .DestModule =  ARC_PDUR_CANTP
    },
    %s
};
const PduRDestPdu_type * const DIAG_P2P_REQ_PduRDestinations[] = {
    &PduR_PduRDestination[0],
    NULL
};
const PduRDestPdu_type * const DIAG_P2P_ACK_PduRDestinations[] = {
    &PduR_PduRDestination[1],
    NULL
};
const PduRDestPdu_type * const DIAG_P2A_REQ_PduRDestinations[] = {
    &PduR_PduRDestination[2],
    NULL
};
const PduRDestPdu_type * const DIAG_P2A_ACK_PduRDestinations[] = {
    &PduR_PduRDestination[3],
    NULL
};
    """%(cstr))
    cstr = ''
    for pdu in GLGet('RxPdu'):
        cstr += """
const PduRDestPdu_type * const PDUR_%s_RX_PduRDestinations[] = {
    &PduR_PduRDestination[PDUR_%s_RX],
    NULL
};\n"""%(GAGet(pdu,'name'),GAGet(pdu,'name'))
    for pdu in GLGet('TxPdu'):
        cstr += """
const PduRDestPdu_type * const PDUR_%s_TX_PduRDestinations[] = {
    &PduR_PduRDestination[PDUR_%s_TX],
    NULL
};\n"""%(GAGet(pdu,'name'),GAGet(pdu,'name'))
    fp.write(cstr)
    cstr = ''
    for pdu in GLGet('RxPdu'):
        cstr += """
const PduRRoutingPath_type PDUR_%s_RX_PduRRoutingPath = {
    .SduLength =  8,
    .SrcPduId =  CANIF_%s_RX,
    .SrcModule =  ARC_PDUR_CANIF,
    .PduRDestPdus =  PDUR_%s_RX_PduRDestinations
};\n"""%(GAGet(pdu,'name'),GAGet(pdu,'name'),GAGet(pdu,'name'))
    for pdu in GLGet('TxPdu'):
        cstr += """
const PduRRoutingPath_type PDUR_%s_TX_PduRRoutingPath = {
    .SduLength =  8,
    .SrcPduId =  COM_%s_TX,
    .SrcModule =  ARC_PDUR_COM,
    .PduRDestPdus =  PDUR_%s_TX_PduRDestinations
};\n"""%(GAGet(pdu,'name'),GAGet(pdu,'name'),GAGet(pdu,'name'))
    fp.write("""
const PduRRoutingPath_type DIAG_P2P_REQ_PduRRoutingPath = {
    .SduLength =  8,
    .SrcPduId =  CANTP_DIAG_P2P_REQ,
    .SrcModule =  ARC_PDUR_CANTP,
    .PduRDestPdus =  DIAG_P2P_REQ_PduRDestinations
};
const PduRRoutingPath_type DIAG_P2P_ACK_PduRRoutingPath = {
    .SduLength =  8,
    .SrcPduId =  DCM_DIAG_P2P_ACK,
    .SrcModule =  ARC_PDUR_DCM,
    .PduRDestPdus =  DIAG_P2P_ACK_PduRDestinations
};

const PduRRoutingPath_type DIAG_P2A_REQ_PduRRoutingPath = {
    .SduLength =  8,
    .SrcPduId =  CANTP_DIAG_P2A_REQ,
    .SrcModule =  ARC_PDUR_CANTP,
    .PduRDestPdus =  DIAG_P2A_REQ_PduRDestinations
};
const PduRRoutingPath_type DIAG_P2A_ACK_PduRRoutingPath = {
    .SduLength =  8,
    .SrcPduId =  DCM_DIAG_P2A_ACK,
    .SrcModule =  ARC_PDUR_DCM,
    .PduRDestPdus =  DIAG_P2A_ACK_PduRDestinations
};
%s\n\n"""%(cstr))
    cstr = ''
    for pdu in GLGet('RxPdu'):
        cstr += '\t&PDUR_%s_RX_PduRRoutingPath,\n'%(GAGet(pdu,'name'))
    for pdu in GLGet('TxPdu'):
        cstr += '\t&PDUR_%s_TX_PduRRoutingPath,\n'%(GAGet(pdu,'name'))
    fp.write("""
const PduRRoutingPath_type * const PduRRoutingPaths[] = { 
    &DIAG_P2P_REQ_PduRRoutingPath,
    &DIAG_P2P_ACK_PduRRoutingPath,
    &DIAG_P2A_REQ_PduRRoutingPath,
    &DIAG_P2A_ACK_PduRRoutingPath,
%s
    NULL
};  

const PduR_PBConfigType PduR_Config = {
    .PduRConfigurationId =  0,
    .NRoutingPaths =  GenPduRId(%s),        // helper
    .RoutingPaths =  PduRRoutingPaths,
    .TpBuffers =  NULL,
    .TpRouteBuffers =  NULL
};

#endif //(PDUR_ZERO_COST_OPERATION == STD_OFF)  
    \n"""%( cstr, len( GLGet('RxPdu')+GLGet('TxPdu') ) ) )
    fp.close() 