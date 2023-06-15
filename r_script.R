### this small R script is for computing some basic statistics on the pivoted results
### 

setwd("/Users/susannecambi/Documents/neuroscience_master/Noce_internship/dev/FWA")
data <- read.csv("pivoted_results.csv")
str(data)

# only remove the "flat" cues (keeping the rows for which there are less than 12 0 values)
data <- data[rowSums(data == 0) < 12, ]

# mean count of associations per cue/word
data[data == 0] <- NA
data$mean_count <- rowMeans(data[ , 14:25], na.rm = TRUE)

# mean count of associations per subject
mean_n_associations <- colMeans(data[ , 14:25], na.rm = T)
n_missing <- colSums(is.na(data[ , 14:25]))
percent_missing <- (colSums(is.na(data[ , 14:25]))/97)*100
subject_stats <- data.frame(n_missing, mean_n_associations, percent_missing)

write.csv(subject_stats, file = "subject_stats.csv")
