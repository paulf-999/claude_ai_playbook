# 🆘 Error recovery — confluence_create_page

## Can't access Confluence space DA

- **Check space exists:** Log in to Confluence and verify `DA` space
- **Check permissions:** Do you have Contributor role in the space?
- **Check MCP:** Run `make enable_mcp server=Atlassian` + restart Claude Code

## Draft review rejected (don't want to publish)

- **Iterate locally:** Make changes to draft and request approval again
- **Or:** Cancel and start over with `/confluence_create_page`

## Page creation fails (MCP error)

- **Check Atlassian MCP is enabled**
- **Check network connection to Confluence**
- **Try again:** Transient errors are common
