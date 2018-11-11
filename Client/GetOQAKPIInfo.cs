public Collection<BSOQAKPI> GetOQAKPIInfo(object objPara, string version)
{
    try
    {
        Collection<BSOQAKPI> col = new Collection<BSOQAKPI>();

        string replyMessage = msgUtil.SendQueryMessage("GetOQAKPIInfo", version, objPara, true);

        // Convert replyMessage to xmlData
        XmlDocument xDoc = new XmlDocument();
        xDoc.LoadXml(replyMessage);

        if (!msgUtil.CheckErrorMessage(xDoc, false))
            return null;

        XmlNodeList list = msgUtil.GetBodyChildNodeList("GetOQAKPIInfo", xDoc);

        foreach (XmlNode node in list)
        {
            BSOQAKPI value = new BSOQAKPI();

            msgUtil.ParseRecivedListMessage(node, value);

            col.Add(value);
        }

        return col;
    }
    catch
    {
        return null;
    }
}

// GetOQAKPIInfo
// -> SendQueryMessage
public string SendQueryMessage(string queryName, string queryVersion, object objPara, bool requestFlag)
        {
            try
            {
            	
            		//Set ConnectionInfo
                ConnectionInfo.MessageName = "GetQueryResult";
                ConnectionInfo.TransactionID = DateTime.Now.ToString("yyyyMMddHHmmssffffff");
                ConnectionInfo.QueryName = queryName;
                ConnectionInfo.QueryVersion = queryVersion;

                string sendMessage = this.CreateQueryMessage(objPara);

                if (requestFlag)
                {
                    string replyMessage = MessageService.This.SendRequest(sendMessage);

                    // Raises a exception when the server can't reply properly or the response has problems we can't handle.
                    if (replyMessage == null || replyMessage.Length <= 0)
                    {
                        throw new EmptyReplyException("The reply message that MES server has sent is empty.")
                        {
                            LabelKey = "ReplyExceptionMessage",
                            MessageKey = "COMM30097",
                            MessageBody = "Client Send Message : " + sendMessage + "\nReply Message Size Zero!!"
                        };
                    }
                    else
                    {
                        return replyMessage;
                    }
                }
            }
            catch (EmptyReplyException idmex)
            {
                throw idmex;
            }
            catch (Exception ex)
            {
                throw ex;
            }

            return null;
        }


// GetOQAKPIInfo
// -> SendQueryMessage
//   -> CreateQueryMessage
private string CreateQueryMessage(object objPara)
        {
            XmlDocument rtnDoc = new XmlDocument();

            StringBuilder sBuilder = new StringBuilder();
            
            
            XmlWriterSettings xws = new XmlWriterSettings();
            xws.Encoding = Encoding.UTF8;
            xws.Indent = true;

						
            XmlWriter writer = XmlWriter.Create(sBuilder, xws);

            // Message
            writer.WriteStartElement("Message");

            
            this.WriteHeaderElement(ref writer);
            

            
            // Body Start
            writer.WriteStartElement("Body");

            writer.WriteStartElement("QUERYID");
            writer.WriteString(ConnectionInfo.QueryName);
            writer.WriteEndElement();

            writer.WriteStartElement("VERSION");
            writer.WriteString(ConnectionInfo.QueryVersion);
            writer.WriteEndElement();

            writer.WriteStartElement("BINDV");

            if (objPara != null)
            {
                Type objType = objPara.GetType();
                PropertyInfo[] objProperties = objType.GetProperties();

                for (int i = 0; i < objProperties.Length; i++)
                {
                    string propertyName = objProperties[i].Name;
                    string propertyType = objProperties[i].PropertyType.ToString();

                    
                    object propertyValue = getPropertyValue(propertyName, objPara);

                    if (propertyValue != null)
                    {
                        writer.WriteStartElement(propertyName);
                        writer.WriteString(propertyValue.ToString());
                        writer.WriteEndElement();
                    }
                    
                }
            }

            writer.WriteEndElement();

            // Body End
            writer.WriteEndElement();
            

            // Message
            writer.WriteEndElement();

            writer.Close();

            return sBuilder.ToString();
        }
        
// GetOQAKPIInfo
// -> SendQueryMessage
//   -> SendRequest

public string SendRequest(string sendMessage)
        {
            try
            {
                Message message;
                if (sendMessage.Contains(GetQueryResult))
                {
                    message = new Message() { SendSubject = messageInfo.QueryTargetSubject };
                }
                else
                {
                    message = new Message() { SendSubject = messageInfo.TargetSubject };
                }
                Message received = transport.SendRequest(message, Double.Parse(messageInfo.TimeOut));
                return (received == null) ? null : received.Value.ToString();
            }
            catch (RendezvousException ex)
            {
                throw ex;
            }
            catch (Exception ex)
            {
                throw ex;
            }
        }
