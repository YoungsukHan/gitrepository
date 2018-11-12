
public static EventInfo makeEventInfo( String eventName, String eventUser, String eventComment, String reasonCodeType, String reasonCode )
	{
		EventInfo eventInfo = new EventInfo();
		eventInfo.setEventName( eventName );
		eventInfo.setEventUser( eventUser );
		eventInfo.setEventTime( TimeStampUtil.getCurrentTimestamp() );
		eventInfo.setEventTimeKey( TimeStampUtil.getCurrentEventTimeKey() );
		if ( eventComment == null ) eventComment = StringUtils.EMPTY;

		eventInfo.setEventComment( eventComment );

		if ( reasonCodeType == null ) reasonCodeType = StringUtils.EMPTY;

		eventInfo.setReasonCodeType( reasonCodeType );

		if ( reasonCode == null ) reasonCode = StringUtils.EMPTY;

		eventInfo.setReasonCode( reasonCode );

		return eventInfo;
	}
	
public class BSOQAKPIServiceImpl extends CommonHistoryServiceDAO<BSOQAKPIKey, BSOQAKPI> implements BSOQAKPIService {


  public void updateBSOQAKPI(EventInfo eventInfo, Document message) {
    try {
      Element bodyElement = message.getDocument().getRootElement().getChild("Body");
      List<Element> ElementList = bodyElement.getChild("BSOQAKPILIST").getChildren("BSOQAKPI");
      for (Element temp : ElementList) {
        // Extract variable value from message.
        
	String  memberNo = temp.getChildText( "MEMBERNO" );
	String  inputDate = temp.getChildText( "INPUTDATE" );


	double  kpiTargetVal = convertChildTextToDouble(temp.getChildText( "KPITARGETVAL" ));
	double  kpiOutputVal = convertChildTextToDouble(temp.getChildText( "KPIOUTPUTVAL" ));
	double  kpiAchievementRate = convertChildTextToDouble(temp.getChildText( "KPIACHIEVEMENTRATE" ));
	double  kpiDetect = convertChildTextToDouble(temp.getChildText( "KPIDETECT" ));
	double  kpiDppm = convertChildTextToDouble(temp.getChildText( "KPIDPPM" ));
	double  kpiTotalVal = convertChildTextToDouble(temp.getChildText( "KPITOTALVAL" ));
	String  commuteNormalYN = temp.getChildText( "COMMUTENORMALYN" );
	String  commuteUnusualType = temp.getChildText( "COMMUTEUNUSUALTYPE" );
	double  commuteTotalVal = convertChildTextToDouble(temp.getChildText( "COMMUTETOTALVAL" ));
	String  detailKpiParam1 = temp.getChildText( "DETAILKPIPARAM1" );
	String  detailKpiParam2 = temp.getChildText( "DETAILKPIPARAM2" );
	String  detailKpiParam3 = temp.getChildText( "DETAILKPIPARAM3" );
	String  detailKpiParam4 = temp.getChildText( "DETAILKPIPARAM4" );
	String  detailKpiParam5 = temp.getChildText( "DETAILKPIPARAM5" );
	String  detailKpiParam6 = temp.getChildText( "DETAILKPIPARAM6" );
	String  detailKpiParam7 = temp.getChildText( "DETAILKPIPARAM7" );
	String  detailKpiParam8 = temp.getChildText( "DETAILKPIPARAM8" );
	String  detailKpiParam9 = temp.getChildText( "DETAILKPIPARAM9" );
	double  detailKpiTotalVal = convertChildTextToDouble(temp.getChildText( "DETAILKPITOTALVAL" ));
	String  plusReason = temp.getChildText( "PLUSREASON" );
	double  plusVal = convertChildTextToDouble(temp.getChildText( "PLUSVAL" ));
	double  plusTotalVal = convertChildTextToDouble(temp.getChildText( "PLUSTOTALVAL" ));
	String  ttl = temp.getChildText( "TTL" );



        // Key Setting

        BSOQAKPIKey BSOQAKPIKey = new BSOQAKPIKey();
        BSOQAKPIKey.setMemberNo(memberNo);
        BSOQAKPIKey.setInputDate(inputDate);

        // Update Or Create Logic

        String sql = StringUtils.EMPTY;
        sql = "SELECT * FROM BSOQAKPI WHERE MEMBERNO=:MEMBERNO AND INPUTDATE=:INPUTDATE";
        HashMap<String, Object> map = new HashMap<String, Object>();
        map.put("MEMBERNO", memberNo);
        map.put("INPUTDATE", inputDate);

        List<HashMap<Object, String>> sqlResult = new ArrayList<HashMap<Object, String>>();
        sqlResult = IDMFrameServiceProxy.getSqlTemplate().queryForList(sql, map);

        BSOQAKPI dataInfo = new BSOQAKPI();

        if (sqlResult.size() > 0) {
          BSOQAKPI oldDataInfo = new BSOQAKPI();
          oldDataInfo = ExtendedObjectProxy.getBSOQAKPIService().selectByKey(BSOQAKPIKey);
          dataInfo = oldDataInfo;

          dataInfo.setKpiTargetVal(kpiTargetVal);
          dataInfo.setKpiOutputVal(kpiOutputVal);
          dataInfo.setKpiAchievementRate(kpiAchievementRate);
          dataInfo.setKpiDetect(kpiDetect);
          dataInfo.setKpiDppm(kpiDppm);
          dataInfo.setKpiTotalVal(kpiTotalVal);
          dataInfo.setCommuteNormalYN(commuteNormalYN);
          dataInfo.setCommuteUnusualType(commuteUnusualType);
          dataInfo.setCommuteTotalVal(commuteTotalVal);
          dataInfo.setDetailKpiParam1(detailKpiParam1);
          dataInfo.setDetailKpiParam2(detailKpiParam2);
          dataInfo.setDetailKpiParam3(detailKpiParam3);
          dataInfo.setDetailKpiParam4(detailKpiParam4);
          dataInfo.setDetailKpiParam5(detailKpiParam5);
          dataInfo.setDetailKpiParam6(detailKpiParam6);
          dataInfo.setDetailKpiParam7(detailKpiParam7);
          dataInfo.setDetailKpiParam8(detailKpiParam8);
          dataInfo.setDetailKpiParam9(detailKpiParam9);
          dataInfo.setDetailKpiTotalVal(detailKpiTotalVal);
          dataInfo.setPlusReason(plusReason);
          dataInfo.setPlusVal(plusVal);
          dataInfo.setPlusTotalVal(plusTotalVal);
          dataInfo.setTtl(ttl);


          ExtendedObjectProxy.getBSOQAKPIService().update(dataInfo);
          
        } else {
          dataInfo.setKey(BSOQAKPIKey);
          dataInfo.setKpiTargetVal(kpiTargetVal);
          dataInfo.setKpiOutputVal(kpiOutputVal);
          dataInfo.setKpiAchievementRate(kpiAchievementRate);
          dataInfo.setKpiDetect(kpiDetect);
          dataInfo.setKpiDppm(kpiDppm);
          dataInfo.setKpiTotalVal(kpiTotalVal);
          dataInfo.setCommuteNormalYN(commuteNormalYN);
          dataInfo.setCommuteUnusualType(commuteUnusualType);
          dataInfo.setCommuteTotalVal(commuteTotalVal);
          dataInfo.setDetailKpiParam1(detailKpiParam1);
          dataInfo.setDetailKpiParam2(detailKpiParam2);
          dataInfo.setDetailKpiParam3(detailKpiParam3);
          dataInfo.setDetailKpiParam4(detailKpiParam4);
          dataInfo.setDetailKpiParam5(detailKpiParam5);
          dataInfo.setDetailKpiParam6(detailKpiParam6);
          dataInfo.setDetailKpiParam7(detailKpiParam7);
          dataInfo.setDetailKpiParam8(detailKpiParam8);
          dataInfo.setDetailKpiParam9(detailKpiParam9);
          dataInfo.setDetailKpiTotalVal(detailKpiTotalVal);
          dataInfo.setPlusReason(plusReason);
          dataInfo.setPlusVal(plusVal);
          dataInfo.setPlusTotalVal(plusTotalVal);
          dataInfo.setTtl(ttl);

          ExtendedObjectProxy.getBSOQAKPIService().insert(dataInfo);
        }
      }

    } catch (Exception e) {
      e.printStackTrace();
    }


  }
	
public void sendReplyBySender( String replySubject, Document doc, String senderName ) throws Exception
	{

		String sReplyMsg = null;
		
		//Set Result Message		
		MessageUtil.setResultItemValue( doc, MessageUtil.Result_ReturnCode, SUCCESS );
		MessageUtil.setResultItemValue( doc, MessageUtil.Result_ErrorMessage, StringUtils.EMPTY );


		//Send Reply
		sReplyMsg = JdomUtils.toString( doc );
		GenericServiceProxy.getGenericSender( senderName ).setDataField( MessageUtil.DataFieldNameXmlData );
		GenericServiceProxy.getGenericSender( senderName ).reply( replySubject, sReplyMsg );
	}
