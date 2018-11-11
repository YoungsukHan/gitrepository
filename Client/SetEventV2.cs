// SetEventV2
public bool SetEventV2(string eventName, object objPara, object objColPara)
        {
            try
            {
                string replyMessage = msgUtil.SendMessage(eventName, objPara, objColPara, true);

                if (replyMessage == "")
                    return false;

                XmlDocument xDoc = new XmlDocument();
                xDoc.LoadXml(replyMessage);

                if (!msgUtil.CheckErrorMessage(xDoc, true, true))
                    return false;

                return true;
            }
            catch (Exception ex)
            {
                throw ex;
            }
        }
        
        
// SetEventV2
//    -> SendMessage
public string SendMessage(string messageName, object objPara, object objColPara, bool requestFlag)
        {
            string responseMsg = null;
            try
            {
            		//Set ConnectionInfo
                ConnectionInfo.MessageName = messageName;
                ConnectionInfo.TransactionID = DateTime.Now.ToString("yyyyMMddHHmmssffffff");

                string sendMessage;
                sendMessage = this.CreateMessage(objPara, objColPara);

                if (requestFlag)
                {
                    responseMsg = MessageService.This.SendRequest(sendMessage);
                    
                    // Raises a exception when the server can't reply properly or the response has problems we can't handle.
                    if (responseMsg == null || responseMsg.Length <= 0)
                    {
                        //sound.PlaySound(SoundUtil.SoundType.ERROR);
                        throw new EmptyReplyException("The reply message that MES server has sent is empty.")
                        {
                            LabelKey = "ReplyExceptionMessage",
                            MessageKey = "COMM30097",
                            MessageBody = "Client Send Message : " + sendMessage + "\nReply Message Size Zero!!"


                        };
                    }
                }
                else
                {
                    MessageService.This.Send(sendMessage);
                }
            }
            catch (Exception ex)
            {
                throw ex;
            }
            finally
            {
                ConnectionInfo.EventComment = string.Empty;
                UILogger.This.Log(UILogger.Message, false, messageName, responseMsg);
            }

            return responseMsg;
        }
